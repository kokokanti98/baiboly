"""
Simple import from GitHub SQL files.
Downloads SQL, modifies it for our schema, and executes it.
"""
import sys
import os
import re
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import create_app, db
from src.models.fihirana import Hira, Tononkira
from sqlalchemy import text


def download_sql(url: str) -> str:
    """Download SQL file from GitHub."""
    print(f"Downloading {url}...")
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def import_collection(sql_content: str, collection: str):
    """Import a collection from SQL content."""
    print(f"\n{'=' * 60}")
    print(f"Importing {collection}")
    print('=' * 60)

    # Parse all INSERT statements
    hira_inserts = []
    tononkira_inserts = []

    # Find all hira inserts to track hira_id sequence
    hira_pattern = r"INSERT INTO hira\s*\([^)]+\)\s*VALUES\s*\(([^)]+)\);"
    for match in re.finditer(hira_pattern, sql_content, re.IGNORECASE):
        hira_inserts.append(match.group(1))

    # Find all tononkira inserts
    tononkira_pattern = r"INSERT INTO tononkira\s*\([^)]+\)\s*VALUES\s*\(([^)]+)\);"
    for match in re.finditer(tononkira_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        tononkira_inserts.append(match.group(1))

    print(f"Found {len(hira_inserts)} hira and {len(tononkira_inserts)} tononkira")

    # Group tononkira by hira_id and extract titles
    tononkira_by_hira = {}
    for values_str in tononkira_inserts:
        # Parse: hira_id, andininy, 'tononkira text', 'fiverenany'
        # Use regex to extract values accounting for quotes and commas in text
        parts = []
        current = ""
        in_quotes = False
        escape_next = False

        for char in values_str:
            if escape_next:
                current += char
                escape_next = False
                continue

            if char == '\\':
                current += char
                escape_next = True
                continue

            if char == "'" and not escape_next:
                in_quotes = not in_quotes
                current += char
            elif char == ',' and not in_quotes:
                parts.append(current.strip())
                current = ""
            else:
                current += char

        if current.strip():
            parts.append(current.strip())

        if len(parts) >= 4:
            hira_id = int(parts[0])
            andininy = int(parts[1])
            tononkira_text = parts[2].strip("'")
            fiverenany = parts[3].strip("'")

            if hira_id not in tononkira_by_hira:
                tononkira_by_hira[hira_id] = []
            tononkira_by_hira[hira_id].append({
                'andininy': andininy,
                'tononkira': tononkira_text,
                'fiverenany': fiverenany.lower() in ('true', '1', 't')
            })

    # Create Hira records
    print("Creating Hira records...")
    for hira_id in sorted(tononkira_by_hira.keys()):
        verses = tononkira_by_hira[hira_id]
        # Get title from first verse
        first_verse = next((v for v in verses if v['andininy'] == 1), verses[0])
        title_text = first_verse['tononkira']
        # Extract first line as title
        title = title_text.split('\\n')[0] if '\\n' in title_text else title_text.split('\n')[0]
        if len(title) > 100:
            title = title[:100] + "..."

        hira = Hira(
            id=hira_id,
            sokajy_id=None,
            lohateny=title,
            isa_andininy=len(verses),
            mpanoratra=None,
            collection=collection
        )
        db.session.add(hira)

        if hira_id % 50 == 0:
            db.session.commit()
            print(f"  Created hira up to #{hira_id}...")

    db.session.commit()
    print(f"✓ Created {len(tononkira_by_hira)} hira")

    # Create Tononkira records
    print("Creating Tononkira records...")
    count = 0
    for hira_id in sorted(tononkira_by_hira.keys()):
        for verse in tononkira_by_hira[hira_id]:
            # Replace \n with actual newline
            tononkira_text = verse['tononkira'].replace('\\n', '\n')
            # Handle escaped quotes
            tononkira_text = tononkira_text.replace("\\'", "'")
            tononkira_text = tononkira_text.replace("''", "'")

            tononkira = Tononkira(
                hira_id=hira_id,
                andininy=verse['andininy'],
                tononkira=tononkira_text,
                fiverenany=verse['fiverenany']
            )
            db.session.add(tononkira)
            count += 1

            if count % 100 == 0:
                db.session.commit()
                print(f"  Created {count} tononkira...")

    db.session.commit()
    print(f"✓ Created {count} tononkira")


def main():
    """Main import function."""
    print("=" * 60)
    print("IMPORT FIHIRANA FROM GITHUB SQL")
    print("=" * 60)

    app = create_app()

    with app.app_context():
        # Check current state
        hira_count = db.session.query(Hira).count()
        tononkira_count = db.session.query(Tononkira).count()

        print(f"\nCurrent state:")
        print(f"  Hira: {hira_count}")
        print(f"  Tononkira: {tononkira_count}")

        if hira_count > 0:
            response = input(f"\n{hira_count} Hira already exist. Clear and re-import? [y/N]: ")
            if response.lower() != 'y':
                print("Import cancelled.")
                return

            print("\nClearing existing data...")
            db.session.execute(text("DELETE FROM tononkira"))
            db.session.execute(text("DELETE FROM hira"))
            db.session.commit()
            print("✓ Cleared")

        # Import collections
        collections = [
            {
                'name': 'FFPM',
                'url': 'https://raw.githubusercontent.com/Rohan29-AN/Fihirana-FFPM/master/sql/01_fihirana_ffpm.sql'
            },
            {
                'name': 'FANAMPINY',
                'url': 'https://raw.githubusercontent.com/Rohan29-AN/Fihirana-FFPM/master/sql/02_fihirana_fanampiny.sql'
            },
            {
                'name': 'ANTEMA',
                'url': 'https://raw.githubusercontent.com/Rohan29-AN/Fihirana-FFPM/master/sql/03_antema.sql'
            }
        ]

        # Ask which collections to import
        print("\nAvailable collections:")
        for i, col in enumerate(collections, 1):
            print(f"  {i}. {col['name']}")

        choice = input("\nImport which collections? (1,2,3 or 'all'): ").strip().lower()

        if choice == 'all':
            selected_collections = collections
        else:
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            selected_collections = [collections[i] for i in indices if 0 <= i < len(collections)]

        # Import each collection
        for collection in selected_collections:
            try:
                sql_content = download_sql(collection['url'])
                import_collection(sql_content, collection['name'])
            except Exception as e:
                print(f"✗ Error importing {collection['name']}: {e}")
                import traceback
                traceback.print_exc()
                db.session.rollback()
                continue

        # Update search vectors
        print("\nUpdating search vectors...")
        db.session.execute(text("""
            UPDATE tononkira
            SET search_vector = to_tsvector('simple', tononkira)
        """))
        db.session.commit()
        print("✓ Search vectors updated")

        # Final statistics
        print("\n" + "=" * 60)
        print("IMPORT COMPLETE")
        print("=" * 60)

        hira_count = db.session.query(Hira).count()
        tononkira_count = db.session.query(Tononkira).count()

        print(f"\nFinal state:")
        print(f"  Hira: {hira_count}")
        print(f"  Tononkira: {tononkira_count}")

        # Show examples by collection
        for collection in selected_collections:
            hiras = db.session.query(Hira).filter_by(collection=collection['name']).limit(3).all()
            if hiras:
                print(f"\n{collection['name']} examples:")
                for hira in hiras:
                    print(f"  #{hira.id}: {hira.lohateny} ({hira.isa_andininy} andininy)")

                    # Show first verse of first example
                    if hiras[0] == hira:
                        first_verse = db.session.query(Tononkira).filter_by(
                            hira_id=hira.id, andininy=1
                        ).first()
                        if first_verse:
                            print(f"     First verse preview:")
                            for line in first_verse.tononkira.split('\n')[:2]:
                                print(f"       {line}")


if __name__ == "__main__":
    main()
