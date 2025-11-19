"""
Import Fihirana from GitHub JSON files.
Much simpler than SQL parsing, and \n are already in the correct format.
"""
import sys
import os
import requests
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import create_app, db
from src.models.fihirana import Hira, Tononkira
from sqlalchemy import text


def download_json(url: str) -> dict:
    """Download JSON file from GitHub."""
    print(f"Downloading {url}...")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def extract_title_from_tononkira(tononkira_text: str) -> str:
    """Extract title from first line before first \n."""
    if '\n' in tononkira_text:
        return tononkira_text.split('\n')[0].strip()
    return tononkira_text[:100].strip()


def import_collection(json_data: dict, collection: str, id_offset: int = 0):
    """
    Import a collection from JSON data.

    Args:
        json_data: Hymn data from JSON file
        collection: Collection name (FFPM, FANAMPINY, ANTEMA)
        id_offset: Offset to add to hymn numbers to avoid ID conflicts
                   FFPM: 0, FANAMPINY: 1000, ANTEMA: 2000
    """
    print(f"\n{'=' * 60}")
    print(f"Importing {collection} (ID offset: {id_offset})")
    print('=' * 60)

    # Count items
    hymn_count = len(json_data)
    print(f"Found {hymn_count} hymns in JSON")

    hira_created = 0
    tononkira_created = 0

    # Iterate through all hymns
    for key, hymn_data in json_data.items():
        # Extract hymn number from key (e.g., "ffpm_1" -> 1)
        laharana = int(hymn_data['laharana'])
        # Add offset to create unique ID across collections
        unique_id = laharana + id_offset

        lohateny = hymn_data.get('lohateny', '')
        mpanoratra = hymn_data.get('mpanoratra', [])
        hira_verses = hymn_data.get('hira', [])

        # If no title provided, extract from first verse
        if not lohateny and hira_verses:
            first_verse = hira_verses[0]
            lohateny = extract_title_from_tononkira(first_verse['tononkira'])

        # Create Hira record with unique ID
        hira = Hira(
            id=unique_id,
            sokajy_id=None,
            lohateny=lohateny,
            isa_andininy=len(hira_verses),
            mpanoratra=', '.join(mpanoratra) if mpanoratra else None,
            collection=collection
        )
        # Store original number as metadata (we'll add a field for this)
        db.session.add(hira)
        hira_created += 1

        # Create Tononkira records for each verse
        for verse in hira_verses:
            tononkira = Tononkira(
                hira_id=unique_id,
                andininy=verse['andininy'],
                tononkira=verse['tononkira'],
                fiverenany=verse.get('fiverenany', False)
            )
            db.session.add(tononkira)
            tononkira_created += 1

        # Commit every 50 hymns
        if hira_created % 50 == 0:
            db.session.commit()
            print(f"  Processed {hira_created}/{hymn_count} hymns...")

    db.session.commit()
    print(f"✓ Created {hira_created} hira (IDs {id_offset+1} to {unique_id})")
    print(f"✓ Created {tononkira_created} tononkira")


def main():
    """Main import function."""
    print("=" * 60)
    print("IMPORT FIHIRANA FROM GITHUB JSON")
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
                'url': 'https://raw.githubusercontent.com/Rohan29-AN/Fihirana-FFPM/master/01_fihirana_ffpm.json'
            },
            {
                'name': 'FANAMPINY',
                'url': 'https://raw.githubusercontent.com/Rohan29-AN/Fihirana-FFPM/master/02_fihirana_fanampiny.json'
            },
            {
                'name': 'ANTEMA',
                'url': 'https://raw.githubusercontent.com/Rohan29-AN/Fihirana-FFPM/master/03_antema.json'
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
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                selected_collections = [collections[i] for i in indices if 0 <= i < len(collections)]
            except (ValueError, IndexError):
                print("Invalid choice. Please enter numbers like '1,2' or 'all'")
                return

        # Define ID offsets for each collection to avoid conflicts
        collection_offsets = {
            'FFPM': 0,
            'FANAMPINY': 1000,
            'ANTEMA': 2000
        }

        # Import each collection
        for collection in selected_collections:
            try:
                json_data = download_json(collection['url'])
                id_offset = collection_offsets.get(collection['name'], 0)
                import_collection(json_data, collection['name'], id_offset)
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

                    # Show first verse preview for first example
                    if hiras[0] == hira:
                        first_verse = db.session.query(Tononkira).filter_by(
                            hira_id=hira.id, andininy=1
                        ).first()
                        if first_verse:
                            print(f"     First verse preview:")
                            lines = first_verse.tononkira.split('\n')
                            for line in lines[:2]:
                                print(f"       {line}")


if __name__ == "__main__":
    main()
