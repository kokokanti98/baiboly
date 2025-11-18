"""
Complete script to import all FFPM (437) and Fanampiny (82) hymns from fihirana.org.
Total: 519 hymns (not 827, that was the old incorrect data).
Gets real titles and lyrics from fihirana.org.
"""
import sys
import os
import time
from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import create_app, db
from src.models.fihirana import Fihirana

BASE_URL = "https://fihirana.org"

# Collection configurations
COLLECTIONS = {
    "FFPM": {"count": 437, "name": "FFPM"},
    "Fanampiny": {"count": 82, "name": "Fanampiny"},
}


def search_hymn_url(numero: int, collection: str) -> Optional[str]:
    """Search for a hymn URL by number and collection."""
    try:
        search_url = f"{BASE_URL}/par-numero/recherche-par-clic/?go_catalog={collection}&go_start={numero}&go_step=1"
        response = requests.get(search_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        collection_lower = collection.lower()
        links = soup.find_all('a', href=True)

        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)

            if f'/{collection_lower}/' in href and href.startswith('http'):
                if text.startswith(f"{numero} -") or text.startswith(f"{numero}.") or text == str(numero):
                    return href

        return None
    except Exception as e:
        print(f"  Error searching #{numero}: {e}")
        return None


def extract_hymn_data(url: str, numero: int, collection: str) -> Optional[Dict[str, any]]:
    """Extract hymn data from individual hymn page."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = None
        h1 = soup.find('h1', class_='entry-title')
        if not h1:
            h1 = soup.find('h1')
        if h1:
            title = h1.get_text(strip=True)

        # Extract lyrics
        content_div = soup.find('div', class_='entry-content')
        if not content_div:
            content_div = soup.find('article')

        if not content_div:
            return None

        paragraphs = content_div.find_all('p')
        verses = []

        for p in paragraphs:
            text = p.get_text(strip=True)
            if (text and len(text) > 15 and
                not text.startswith('Publié') and
                not text.startswith('Auteur') and
                not text.startswith('Catégorie') and
                'Share this' not in text):
                verses.append(text)

        paroles = '\n\n'.join(verses) if verses else ''

        if not paroles or len(paroles) < 50:
            return None

        return {
            'numero': numero,
            'titre': title or f"Fihirana {numero}",
            'paroles': paroles,
            'collection': collection
        }
    except Exception as e:
        print(f"  Error extracting #{numero}: {e}")
        return None


def import_collection(collection: str, total_count: int):
    """Import all hymns from a collection."""
    print(f"\n{'='*60}")
    print(f"Importing {collection} collection (1-{total_count})...")
    print(f"{'='*60}")

    imported = 0
    failed = 0

    for numero in range(1, total_count + 1):
        print(f"\n[{numero}/{total_count}] Processing {collection} #{numero}...", end=' ')

        # Check if already exists
        existing = db.session.query(Fihirana).filter(
            Fihirana.collection == collection,
            Fihirana.numero == numero
        ).first()

        if existing:
            print(f"✓ Exists")
            imported += 1
            continue

        # Search for URL
        url = search_hymn_url(numero, collection)
        if not url:
            print(f"✗ Not found")
            failed += 1
            time.sleep(1)
            continue

        # Extract data
        hymn_data = extract_hymn_data(url, numero, collection)
        if not hymn_data:
            print(f"✗ No data")
            failed += 1
            time.sleep(1)
            continue

        # Save to database
        fihirana = Fihirana(
            numero=hymn_data['numero'],
            titre=hymn_data['titre'],
            paroles=hymn_data['paroles'],
            collection=collection
        )

        db.session.add(fihirana)
        imported += 1

        # Show title
        title_short = hymn_data['titre'][:40] + '...' if len(hymn_data['titre']) > 40 else hymn_data['titre']
        print(f"✓ {title_short}")

        # Commit every 10 hymns
        if imported % 10 == 0:
            try:
                db.session.commit()
            except Exception as e:
                print(f"\n  Error committing: {e}")
                db.session.rollback()

        # Be nice to server
        time.sleep(2)

    # Final commit
    try:
        db.session.commit()
        print(f"\n✓ Imported {imported} hymns from {collection}")
        print(f"✗ Failed: {failed}")
    except Exception as e:
        db.session.rollback()
        print(f"ERROR committing: {e}")

    return imported


def main():
    """Main import function."""
    print("\n" + "="*60)
    print("COMPLETE FIHIRANA IMPORT FROM FIHIRANA.ORG")
    print("="*60)
    print("\nImporting all hymns with correct titles:")
    print("  - FFPM: 437 hymns")
    print("  - Fanampiny: 82 hymns")
    print("  - Total: 519 hymns\n")
    print("This will take approximately 30-40 minutes...")
    print("="*60)

    app = create_app()

    with app.app_context():
        # Don't clear - just add/update
        existing_count = db.session.query(Fihirana).count()
        print(f"\nCurrent database: {existing_count} hymns")

        total_imported = 0

        # Import FFPM
        imported = import_collection("FFPM", COLLECTIONS["FFPM"]["count"])
        total_imported += imported

        # Import Fanampiny
        imported = import_collection("Fanampiny", COLLECTIONS["Fanampiny"]["count"])
        total_imported += imported

        # Statistics
        print("\n" + "="*60)
        print("IMPORT COMPLETE")
        print("="*60)

        ffpm_count = db.session.query(Fihirana).filter(Fihirana.collection == 'FFPM').count()
        fanampiny_count = db.session.query(Fihirana).filter(Fihirana.collection == 'Fanampiny').count()
        total_count = db.session.query(Fihirana).count()

        print(f"\nDatabase statistics:")
        print(f"  FFPM:      {ffpm_count} hymns")
        print(f"  Fanampiny: {fanampiny_count} hymns")
        print(f"  TOTAL:     {total_count} hymns")

        # Show examples
        print(f"\nExamples from FFPM:")
        examples = db.session.query(Fihirana).filter(Fihirana.collection == 'FFPM').limit(5).all()
        for ex in examples:
            print(f"  #{ex.numero}: {ex.titre}")

        print(f"\nExamples from Fanampiny:")
        examples = db.session.query(Fihirana).filter(Fihirana.collection == 'Fanampiny').limit(5).all()
        for ex in examples:
            print(f"  #{ex.numero}: {ex.titre}")
        print()


if __name__ == "__main__":
    main()
