"""
Simple script to scrape fihirana.org by trying each hymn number directly.
Uses the search page to get the actual URLs.
"""
import sys
import os
import time
import re
from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import create_app, db
from src.models.fihirana import Fihirana

BASE_URL = "https://fihirana.org"


def search_hymn_url(numero: int, collection: str) -> Optional[str]:
    """
    Search for a hymn URL by number and collection.
    Uses the search results page.
    """
    try:
        # The search page with specific number
        search_url = f"{BASE_URL}/par-numero/recherche-par-clic/?go_catalog={collection}&go_start={numero}&go_step=1"

        response = requests.get(search_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links
        links = soup.find_all('a', href=True)

        collection_lower = collection.lower()

        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)

            # Check if this link contains our number and collection
            if f'/{collection_lower}/' in href and href.startswith('http'):
                # Check if the text starts with our number
                if text.startswith(f"{numero} -") or text.startswith(f"{numero}.") or text == str(numero):
                    return href

        return None

    except Exception as e:
        print(f"  Error searching for #{numero}: {e}")
        return None


def extract_hymn_data(url: str, numero: int, collection: str) -> Optional[Dict[str, any]]:
    """
    Extract hymn data from individual hymn page.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title from <h1>
        title = None
        h1 = soup.find('h1', class_='entry-title')
        if not h1:
            h1 = soup.find('h1')

        if h1:
            title = h1.get_text(strip=True)

        # Extract lyrics from entry-content
        content_div = soup.find('div', class_='entry-content')
        if not content_div:
            content_div = soup.find('article')

        if not content_div:
            return None

        # Extract all paragraphs (verses)
        paragraphs = content_div.find_all('p')
        verses = []

        for p in paragraphs:
            text = p.get_text(strip=True)
            # Skip empty, short, and metadata paragraphs
            if (text and
                len(text) > 15 and
                not text.startswith('Publié') and
                not text.startswith('Auteur') and
                not text.startswith('Catégorie') and
                'Share this' not in text):
                verses.append(text)

        # Combine verses into lyrics
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


def import_collection(collection: str, start: int = 1, end: int = 20):
    """
    Import hymns from a collection by number range.
    """
    print(f"\n{'='*60}")
    print(f"Importing {collection} collection (#{start}-#{end})...")
    print(f"{'='*60}")

    imported = 0
    failed = 0

    for numero in range(start, end + 1):
        print(f"\n[{numero-start+1}/{end-start+1}] Processing Fihirana #{numero}...")

        # Check if already exists
        existing = db.session.query(Fihirana).filter(
            Fihirana.collection == collection,
            Fihirana.numero == numero
        ).first()

        if existing:
            print(f"  Already exists, skipping...")
            continue

        # Search for the hymn URL
        url = search_hymn_url(numero, collection)

        if not url:
            print(f"  ✗ URL not found")
            failed += 1
            continue

        print(f"  Found: {url}")

        # Extract data from page
        hymn_data = extract_hymn_data(url, numero, collection)

        if not hymn_data:
            print(f"  ✗ Could not extract data")
            failed += 1
            continue

        # Create fihirana entry
        fihirana = Fihirana(
            numero=hymn_data['numero'],
            titre=hymn_data['titre'],
            paroles=hymn_data['paroles'],
            collection=collection
        )

        db.session.add(fihirana)
        imported += 1

        print(f"  ✓ Imported: {hymn_data['titre'][:50]}...")

        # Commit every 5 hymns
        if imported % 5 == 0:
            print(f"  Committing batch...")
            db.session.commit()

        # Be nice to the server
        time.sleep(2)

    # Final commit
    try:
        db.session.commit()
        print(f"\n✓ Successfully imported {imported} fihirana from {collection}")
        print(f"✗ Failed: {failed}")
    except Exception as e:
        db.session.rollback()
        print(f"ERROR committing {collection}: {e}")
        return 0

    return imported


def main():
    """Main import function."""
    print("\n" + "="*60)
    print("FIHIRANA.ORG SIMPLE SCRAPER")
    print("="*60)
    print("\nThis will import hymns from fihirana.org with correct titles.")
    print("Starting with first 30 FFPM hymns as a test...\n")

    app = create_app()

    with app.app_context():
        # Clear old data
        print("\nClearing old Fihirana data...")
        deleted = db.session.query(Fihirana).delete()
        db.session.commit()
        print(f"✓ Cleared {deleted} old entries")

        # Import first 30 FFPM hymns for testing
        total_imported = import_collection("FFPM", start=1, end=30)

        # Print final statistics
        print("\n" + "="*60)
        print("IMPORT COMPLETE")
        print("="*60)
        print(f"Total fihirana imported: {total_imported}")

        # Query database for stats
        ffpm_count = db.session.query(Fihirana).filter(Fihirana.collection == 'FFPM').count()
        total_count = db.session.query(Fihirana).count()

        print(f"\nDatabase statistics:")
        print(f"  FFPM:      {ffpm_count} fihirana")
        print(f"  TOTAL:     {total_count} fihirana")

        # Show some examples
        print(f"\nExamples:")
        examples = db.session.query(Fihirana).limit(3).all()
        for ex in examples:
            print(f"  #{ex.numero}: {ex.titre}")
        print()


if __name__ == "__main__":
    main()
