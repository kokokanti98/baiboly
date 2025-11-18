"""
Script to import Fihirana (hymns) data from GitHub repository.
Imports FFPM, Fanampiny, and Antema hymns into the database.
"""
import sys
import os
import requests
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import create_app, db
from src.models.fihirana import Fihirana

# GitHub repository URLs
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Rohan29-AN/Fihirana-FFPM/master"

# Collections to import
COLLECTIONS = {
    "ffpm": {
        "name": "FFPM",
        "url": f"{GITHUB_BASE_URL}/01_fihirana_ffpm.json",
        "count": 437
    },
    "fanampiny": {
        "name": "Fanampiny",
        "url": f"{GITHUB_BASE_URL}/02_fihirana_fanampiny.json",
        "count": 82
    },
    "antema": {
        "name": "Antema",
        "url": f"{GITHUB_BASE_URL}/03_fihirana_antema.json",
        "count": 117
    }
}


def download_fihirana_data(url: str) -> dict:
    """Download fihirana JSON data from GitHub."""
    print(f"Downloading from {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def import_collection(collection_key: str, collection_info: dict):
    """Import a single collection of fihirana."""
    print(f"\n{'='*60}")
    print(f"Importing {collection_info['name']} collection...")
    print(f"{'='*60}")

    try:
        data = download_fihirana_data(collection_info['url'])
    except Exception as e:
        print(f"ERROR downloading {collection_info['name']}: {e}")
        return 0

    imported = 0

    # Check if data is a list or dict
    if isinstance(data, list):
        hymns_list = data
    elif isinstance(data, dict):
        # If it's a dict, values should be the hymns
        hymns_list = list(data.values()) if data else []
    else:
        print(f"ERROR: Unexpected data format for {collection_info['name']}")
        return 0

    for hymn_data in hymns_list:
        try:
            # Extract hymn information
            # Format might vary, handle different structures
            if isinstance(hymn_data, dict):
                # Try different field names (laharana is Malagasy for number)
                numero = hymn_data.get('laharana') or hymn_data.get('numero') or hymn_data.get('number') or hymn_data.get('id', 0)
                titre = hymn_data.get('lohateny') or hymn_data.get('titre') or hymn_data.get('title', 'Sans titre')

                # Combine verses from hira array into single text
                paroles = ''
                hira_array = hymn_data.get('hira', [])
                if hira_array and isinstance(hira_array, list):
                    # Join all verses
                    verses = []
                    for verse in hira_array:
                        if isinstance(verse, dict):
                            tononkira = verse.get('tononkira', '')
                            if tononkira:
                                andininy = verse.get('andininy', '')
                                verses.append(f"{andininy}. {tononkira}" if andininy else tononkira)
                    paroles = '\n\n'.join(verses)

                # Fallback to other fields if hira not found
                if not paroles:
                    paroles = hymn_data.get('paroles') or hymn_data.get('lyrics') or hymn_data.get('text') or hymn_data.get('content', '')

                # Skip if no number or lyrics
                if not numero or not paroles:
                    continue

                # Check if already exists
                existing = db.session.query(Fihirana).filter(
                    Fihirana.collection == collection_info['name'],
                    Fihirana.numero == numero
                ).first()

                if existing:
                    print(f"  Fihirana #{numero} already exists, skipping...")
                    continue

                # Create fihirana entry
                fihirana = Fihirana(
                    numero=int(numero),
                    titre=str(titre),
                    paroles=str(paroles),
                    collection=collection_info['name']
                )

                db.session.add(fihirana)
                imported += 1

                if imported % 50 == 0:
                    print(f"  Imported {imported} fihirana...")
                    db.session.flush()

        except Exception as e:
            print(f"  ERROR importing hymn: {e}")
            continue

    try:
        db.session.commit()
        print(f"\n✓ Successfully imported {imported} fihirana from {collection_info['name']}")
    except Exception as e:
        db.session.rollback()
        print(f"ERROR committing {collection_info['name']}: {e}")
        return 0

    return imported


def main():
    """Main import function."""
    print("\n" + "="*60)
    print("FIHIRANA DATA IMPORT")
    print("="*60)

    app = create_app()

    with app.app_context():
        total_imported = 0

        for collection_key, collection_info in COLLECTIONS.items():
            imported = import_collection(collection_key, collection_info)
            total_imported += imported

        # Print final statistics
        print("\n" + "="*60)
        print("IMPORT COMPLETE")
        print("="*60)
        print(f"Total fihirana imported: {total_imported}")

        # Query database for stats
        ffpm_count = db.session.query(Fihirana).filter(Fihirana.collection == 'FFPM').count()
        fanampiny_count = db.session.query(Fihirana).filter(Fihirana.collection == 'Fanampiny').count()
        antema_count = db.session.query(Fihirana).filter(Fihirana.collection == 'Antema').count()
        total_count = db.session.query(Fihirana).count()

        print(f"\nDatabase statistics:")
        print(f"  FFPM:      {ffpm_count} fihirana")
        print(f"  Fanampiny: {fanampiny_count} fihirana")
        print(f"  Antema:    {antema_count} fihirana")
        print(f"  TOTAL:     {total_count} fihirana")
        print()


if __name__ == "__main__":
    main()
