"""
Migrate legacy Fihirana data to new verse-based structure.
Extracts verses from paroles text and creates Hira + Tononkira records.
"""
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import create_app, db
from src.models.fihirana import Fihirana, Hira, Tononkira


def extract_title_from_paroles(paroles: str) -> str:
    """
    Extract title from first line of paroles.
    Format: "1. Title text..."
    Returns: "Title text"
    """
    lines = paroles.split('\n')
    if lines:
        first_line = lines[0].strip()
        # Remove verse number if present
        match = re.match(r'^\d+\.\s*(.+)$', first_line)
        if match:
            return match.group(1)
        return first_line
    return ""


def parse_verses(paroles: str) -> list:
    """
    Parse paroles text into verses.

    Format example:
    1. Line 1
       Line 2

    2. Line 1
       Line 2

    Returns list of dicts: [{andininy: 1, text: "Line 1\nLine 2"}, ...]
    """
    verses = []
    current_verse = None
    current_text = []

    lines = paroles.split('\n')

    for line in lines:
        line_stripped = line.strip()

        if not line_stripped:
            continue

        # Check if this is a verse number line (starts with "N.")
        verse_match = re.match(r'^(\d+)\.\s*(.*)$', line_stripped)

        if verse_match:
            # Save previous verse
            if current_verse is not None and current_text:
                verses.append({
                    'andininy': current_verse,
                    'text': '\n'.join(current_text),
                    'fiverenany': False
                })

            # Start new verse
            current_verse = int(verse_match.group(1))
            verse_line = verse_match.group(2)
            current_text = [verse_line] if verse_line else []
        else:
            # Continuation of current verse
            if current_verse is not None:
                current_text.append(line_stripped)

    # Save last verse
    if current_verse is not None and current_text:
        verses.append({
            'andininy': current_verse,
            'text': '\n'.join(current_text),
            'fiverenany': False
        })

    return verses


def migrate_fihirana_to_hira(fihirana: Fihirana) -> Hira:
    """
    Migrate a legacy Fihirana to new Hira + Tononkira structure.
    """
    # Extract title from paroles
    title = extract_title_from_paroles(fihirana.paroles)
    if not title:
        title = fihirana.titre

    # Parse verses
    verses_data = parse_verses(fihirana.paroles)

    if not verses_data:
        # If no verses found, create single verse with all paroles
        verses_data = [{
            'andininy': 1,
            'text': fihirana.paroles,
            'fiverenany': False
        }]

    # Create Hira
    hira = Hira(
        id=fihirana.numero,
        sokajy_id=None,
        lohateny=title,
        isa_andininy=len(verses_data),
        mpanoratra=None,
        collection=fihirana.collection
    )

    db.session.add(hira)

    # Create Tononkira for each verse
    for verse_data in verses_data:
        tononkira = Tononkira(
            hira_id=hira.id,
            andininy=verse_data['andininy'],
            tononkira=verse_data['text'],
            fiverenany=verse_data['fiverenany']
        )
        db.session.add(tononkira)

    return hira


def main():
    """Main migration function."""
    print("=" * 60)
    print("MIGRATE LEGACY FIHIRANA TO VERSE STRUCTURE")
    print("=" * 60)

    app = create_app()

    with app.app_context():
        # Check current state
        legacy_count = db.session.query(Fihirana).count()
        hira_count = db.session.query(Hira).count()

        print(f"\nCurrent state:")
        print(f"  Legacy Fihirana: {legacy_count}")
        print(f"  New Hira: {hira_count}")

        if legacy_count == 0:
            print("\nNo legacy data to migrate!")
            return

        if hira_count > 0:
            response = input(f"\n{hira_count} Hira already exist. Clear and re-migrate? [y/N]: ")
            if response.lower() != 'y':
                print("Migration cancelled.")
                return

            print("\nClearing existing Hira and Tononkira...")
            db.session.query(Tononkira).delete()
            db.session.query(Hira).delete()
            db.session.commit()
            print("✓ Cleared")

        # Migrate all Fihirana
        print(f"\nMigrating {legacy_count} Fihirana...")

        fihiranas = db.session.query(Fihirana).order_by(Fihirana.numero).all()
        migrated = 0

        for fihirana in fihiranas:
            try:
                hira = migrate_fihirana_to_hira(fihirana)
                migrated += 1

                if migrated % 10 == 0:
                    db.session.commit()
                    print(f"  Migrated {migrated}/{legacy_count}...")
            except Exception as e:
                print(f"  Error migrating #{fihirana.numero}: {e}")
                continue

        db.session.commit()

        # Update search vectors
        print("\nUpdating search vectors...")
        from sqlalchemy import text
        db.session.execute(text("""
            UPDATE tononkira
            SET search_vector = to_tsvector('simple', tononkira)
        """))
        db.session.commit()

        # Final statistics
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETE")
        print("=" * 60)

        hira_count = db.session.query(Hira).count()
        tononkira_count = db.session.query(Tononkira).count()

        print(f"\nFinal state:")
        print(f"  Hira: {hira_count}")
        print(f"  Tononkira: {tononkira_count}")

        # Show examples
        print(f"\nExamples:")
        examples = db.session.query(Hira).limit(5).all()
        for hira in examples:
            print(f"  #{hira.id}: {hira.lohateny} ({hira.isa_andininy} andininy)")
        print()


if __name__ == "__main__":
    main()
