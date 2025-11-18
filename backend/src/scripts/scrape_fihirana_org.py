"""
Script to scrape fihirana.org for correct hymn data with titles.
Gets FFPM, Fanampiny, and Antema collections.
"""
import sys
import os
import time
import re
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import create_app, db
from src.models.fihirana import Fihirana

# Base URL
BASE_URL = "https://fihirana.org"

# Collections to scrape
COLLECTIONS = {
    "FFPM": {
        "name": "FFPM",
        "start": 1,
        "end": 437,  # FFPM has 437 hymns
        "url_template": f"{BASE_URL}/ffpm/page/{{page}}/"
    },
    "Fanampiny": {
        "name": "Fanampiny",
        "start": 1,
        "end": 82,  # Fanampiny has 82 hymns
        "url_template": f"{BASE_URL}/fanampiny/page/{{page}}/"
    },
    "Antema": {
        "name": "Antema",
        "start": 1,
        "end": 117,  # Antema has 117 hymns
        "url_template": f"{BASE_URL}/antema/page/{{page}}/"
    }
}


def get_hymn_links_from_list(collection: str, max_hymns: int = 500) -> List[Dict[str, any]]:
    """
    Get all hymn links from the collection list page.
    """
    print(f"\nFetching hymn links for {collection}...")

    collection_lower = collection.lower()
    base_url = f"{BASE_URL}/par-numero/recherche-par-clic/?go_catalog={collection}"

    hymns = []

    try:
        # Try to get the main list page
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all hymn links in the number list
        # The structure is: <a href="url">Number</a>
        links = soup.find_all('a', href=True)

        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)

            # Check if this is a hymn link (contains the collection name in URL)
            if f'/{collection_lower}/' in href and href.startswith('http'):
                # Try to extract number from link text
                try:
                    numero = int(text)
                    hymns.append({
                        'numero': numero,
                        'url': href,
                        'collection': collection
                    })
                except (ValueError, TypeError):
                    # Not a number, skip
                    continue

        print(f"Found {len(hymns)} hymn links for {collection}")

    except Exception as e:
        print(f"Error fetching list for {collection}: {e}")

    return hymns


def extract_hymn_data(url: str, numero: int, collection: str) -> Optional[Dict[str, any]]:
    """
    Extract hymn data from individual hymn page.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title from <h1> or <title>
        title = None
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text(strip=True)

        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                # Clean up title (remove site name, etc.)
                title = title.split('|')[0].strip()
                title = title.split('-')[0].strip()

        # Extract lyrics from the content
        # Look for div with class 'entry-content' or similar
        content_div = soup.find('div', class_='entry-content')
        if not content_div:
            content_div = soup.find('article')

        if not content_div:
            print(f"  Warning: No content found for #{numero}")
            return None

        # Extract all paragraphs (verses)
        paragraphs = content_div.find_all('p')
        verses = []

        for p in paragraphs:
            text = p.get_text(strip=True)
            # Skip empty paragraphs and metadata
            if text and len(text) > 10 and not text.startswith('Publié'):
                verses.append(text)

        # Combine verses into lyrics
        paroles = '\n\n'.join(verses) if verses else ''

        if not paroles:
            print(f"  Warning: No lyrics found for #{numero}")
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


def import_collection(collection: str):
    """
    Import all hymns from a collection.
    """
    print(f"\n{'='*60}")
    print(f"Importing {collection} collection...")
    print(f"{'='*60}")

    # Get all hymn links
    hymns_info = get_hymn_links_from_list(collection, max_hymns=500)

    if not hymns_info:
        print(f"No hymns found for {collection}")
        return 0

    imported = 0

    for idx, hymn_info in enumerate(hymns_info[:20], 1):  # Start with first 20 for testing
        numero = hymn_info['numero']
        url = hymn_info['url']

        print(f"\n[{idx}/{len(hymns_info[:20])}] Processing Fihirana #{numero}...")

        # Check if already exists
        existing = db.session.query(Fihirana).filter(
            Fihirana.collection == collection,
            Fihirana.numero == numero
        ).first()

        if existing:
            print(f"  Already exists, skipping...")
            continue

        # Extract data from page
        hymn_data = extract_hymn_data(url, numero, collection)

        if not hymn_data:
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

        # Commit every 10 hymns
        if imported % 10 == 0:
            print(f"  Committing batch...")
            db.session.commit()

        # Be nice to the server
        time.sleep(1)

    # Final commit
    try:
        db.session.commit()
        print(f"\n✓ Successfully imported {imported} fihirana from {collection}")
    except Exception as e:
        db.session.rollback()
        print(f"ERROR committing {collection}: {e}")
        return 0

    return imported


def main():
    """Main import function."""
    print("\n" + "="*60)
    print("FIHIRANA.ORG DATA SCRAPER")
    print("="*60)

    app = create_app()

    with app.app_context():
        # Clear old data
        print("\nClearing old Fihirana data...")
        db.session.query(Fihirana).delete()
        db.session.commit()
        print("✓ Old data cleared")

        total_imported = 0

        # Import FFPM first (testing with 20)
        imported = import_collection("FFPM")
        total_imported += imported

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
        print()


if __name__ == "__main__":
    main()
