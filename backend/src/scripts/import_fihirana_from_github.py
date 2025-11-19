"""
Import Fihirana FFPM hymns from GitHub SQL file.
Source: https://github.com/Rohan29-AN/Fihirana-FFPM/blob/master/sql/01_fihirana_ffpm.sql

Structure:
- sokajy (category): id, anarana
- hira (hymn): id, sokajy_id, lohateny, isa_andininy, mpanoratra
- tononkira (verse): id, hira_id, andininy, tononkira, fiverenany

The title is extracted from the first verse (text before first \n).
"""
import sys
import os
import re
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import create_app, db
from src.models.fihirana import Sokajy, Hira, Tononkira

SQL_URL = "https://raw.githubusercontent.com/Rohan29-AN/Fihirana-FFPM/master/sql/01_fihirana_ffpm.sql"


def parse_sql_values_line(line: str) -> tuple:
    """
    Parse a single VALUES line from SQL.

    Example line:
    INSERT INTO tononkira (hira_id, andininy, tononkira, fiverenany)VALUES (1, 1, 'Text here', 'False');

    Returns:
        Tuple of values
    """
    # Find the VALUES(...) part
    match = re.search(r'VALUES\s*\((.*?)\);?\s*$', line, re.IGNORECASE)
    if not match:
        return None

    values_str = match.group(1)

    # Split by comma, handling quotes
    values = []
    current = ""
    in_quotes = False
    escape_next = False

    for char in values_str:
        if escape_next:
            current += char
            escape_next = False
        elif char == '\\':
            current += char
            escape_next = True
        elif char == "'" and not escape_next:
            in_quotes = not in_quotes
            # Don't add the quotes themselves
        elif char == ',' and not in_quotes:
            values.append(current.strip())
            current = ""
        else:
            current += char

    # Add last value
    if current.strip():
        values.append(current.strip())

    return tuple(values)


def extract_title_from_verse(verse_text: str) -> str:
    """
    Extract title from first verse (text before first \n).

    Example:
    'Andriananahary masina indrindra!\nNy anjelinao...'
    Returns: 'Andriananahary masina indrindra!'
    """
    lines = verse_text.split('\\n')
    return lines[0] if lines else verse_text


def download_sql_file() -> str:
    """Download SQL file from GitHub."""
    print(f"Downloading SQL file from {SQL_URL}...")
    response = requests.get(SQL_URL, timeout=30)
    response.raise_for_status()
    print(f"✓ Downloaded {len(response.text)} characters")
    return response.text


def parse_and_import(sql_content: str):
    """Parse SQL file line by line and import into database."""

    lines = sql_content.split('\n')

    sokajy_count = 0
    hira_count = 0
    tononkira_count = 0
    hira_data = {}  # Store for later title extraction

    print(f"\nParsing {len(lines)} lines...")

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('--'):
            continue

        try:
            # Sokajy inserts
            if 'INSERT INTO sokajy' in line:
                values = parse_sql_values_line(line)
                if values and len(values) >= 2:
                    sokajy_id = int(values[0])
                    anarana = values[1]

                    existing = db.session.query(Sokajy).filter_by(id=sokajy_id).first()
                    if not existing:
                        sokajy = Sokajy(id=sokajy_id, anarana=anarana)
                        db.session.add(sokajy)
                        sokajy_count += 1

            # Hira inserts
            elif 'INSERT INTO hira' in line:
                values = parse_sql_values_line(line)
                if values and len(values) >= 4:
                    hira_id = int(values[0])
                    sokajy_id = int(values[1]) if values[1] and values[1] != 'NULL' else None
                    lohateny = values[2] if values[2] else f"Fihirana {hira_id}"
                    isa_andininy = int(values[3]) if values[3] else 0
                    mpanoratra = values[4] if len(values) > 4 and values[4] and values[4] != 'NULL' else None

                    existing = db.session.query(Hira).filter_by(id=hira_id).first()
                    if not existing:
                        hira = Hira(
                            id=hira_id,
                            sokajy_id=sokajy_id,
                            lohateny=lohateny,
                            isa_andininy=isa_andininy,
                            mpanoratra=mpanoratra,
                            collection='FFPM'
                        )
                        db.session.add(hira)
                        hira_data[hira_id] = {'lohateny': lohateny, 'first_verse': None}
                        hira_count += 1

                        if hira_count % 10 == 0:
                            print(f"  Imported {hira_count} hira...")
                            db.session.commit()

            # Tononkira inserts
            elif 'INSERT INTO tononkira' in line:
                values = parse_sql_values_line(line)
                if values and len(values) >= 4:
                    hira_id = int(values[0])
                    andininy = int(values[1])
                    tononkira_text = values[2].replace('\\n', '\n')  # Convert \n to actual newlines
                    fiverenany_str = values[3].lower()
                    fiverenany = fiverenany_str == 'true'

                    # Extract title from first verse
                    if hira_id in hira_data and andininy == 1 and not fiverenany:
                        title = extract_title_from_verse(values[2])  # Use original with \n
                        hira_data[hira_id]['first_verse'] = title

                    existing = db.session.query(Tononkira).filter_by(
                        hira_id=hira_id, andininy=andininy
                    ).first()

                    if not existing:
                        tononkira = Tononkira(
                            hira_id=hira_id,
                            andininy=andininy,
                            tononkira=tononkira_text,
                            fiverenany=fiverenany
                        )
                        db.session.add(tononkira)
                        tononkira_count += 1

                        if tononkira_count % 100 == 0:
                            print(f"  Imported {tononkira_count} tononkira...")
                            db.session.commit()

        except Exception as e:
            print(f"  Error on line {line_num}: {e}")
            continue

    db.session.commit()

    print(f"\n✓ Imported {sokajy_count} sokajy")
    print(f"✓ Imported {hira_count} hira")
    print(f"✓ Imported {tononkira_count} tononkira")

    # Update titles from first verses
    print(f"\nUpdating titles from first verses...")
    updated = 0
    for hira_id, data in hira_data.items():
        if data['first_verse']:
            hira = db.session.query(Hira).filter_by(id=hira_id).first()
            if hira:
                hira.lohateny = data['first_verse']
                updated += 1

    db.session.commit()
    print(f"✓ Updated {updated} titles")

    # Update search vectors
    print(f"\nUpdating search vectors...")
    db.session.execute("""
        UPDATE tononkira
        SET search_vector = to_tsvector('simple', tononkira)
    """)
    db.session.commit()
    print(f"✓ Search vectors updated")


def main():
    """Main import function."""
    print("=" * 60)
    print("FIHIRANA FFPM IMPORT FROM GITHUB")
    print("=" * 60)
    print(f"\nSource: {SQL_URL}")

    app = create_app()

    with app.app_context():
        # Check current data
        sokajy_count = db.session.query(Sokajy).count()
        hira_count = db.session.query(Hira).count()
        tononkira_count = db.session.query(Tononkira).count()

        print(f"\nCurrent database:")
        print(f"  Sokajy:    {sokajy_count}")
        print(f"  Hira:      {hira_count}")
        print(f"  Tononkira: {tononkira_count}")

        if hira_count > 0:
            response = input("\nData already exists. Clear and re-import? [y/N]: ")
            if response.lower() == 'y':
                print("\nClearing existing data...")
                db.session.query(Tononkira).delete()
                db.session.query(Hira).delete()
                db.session.query(Sokajy).delete()
                db.session.commit()
                print("✓ Cleared")
            else:
                print("Import cancelled.")
                return

        # Download and parse SQL
        try:
            sql_content = download_sql_file()
            parse_and_import(sql_content)
        except Exception as e:
            print(f"\nError: {e}")
            db.session.rollback()
            return

        # Show final statistics
        print("\n" + "=" * 60)
        print("IMPORT COMPLETE")
        print("=" * 60)

        sokajy_count = db.session.query(Sokajy).count()
        hira_count = db.session.query(Hira).count()
        tononkira_count = db.session.query(Tononkira).count()

        print(f"\nFinal database:")
        print(f"  Sokajy:    {sokajy_count}")
        print(f"  Hira:      {hira_count}")
        print(f"  Tononkira: {tononkira_count}")

        # Show examples
        print(f"\nExamples:")
        examples = db.session.query(Hira).limit(5).all()
        for hira in examples:
            print(f"  #{hira.id}: {hira.lohateny} ({hira.isa_andininy} andininy)")
            if hira.tononkira:
                first_verse = hira.tononkira[0]
                preview = first_verse.tononkira[:60] + "..." if len(first_verse.tononkira) > 60 else first_verse.tononkira
                print(f"       {preview.replace(chr(10), ' ')}")
        print()


if __name__ == "__main__":
    main()
