"""
Quick import of first 100 FFPM hymns for immediate testing.
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


def search_hymn_url(numero: int, collection: str) -> Optional[str]:
    """Search for a hymn URL."""
    try:
        search_url = f"{BASE_URL}/par-numero/recherche-par-clic/?go_catalog={collection}&go_start={numero}&go_step=1"
        response = requests.get(search_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        collection_lower = collection.lower()
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            if f'/{collection_lower}/' in href and href.startswith('http'):
                if text.startswith(f"{numero} -") or text.startswith(f"{numero}."):
                    return href
        return None
    except:
        return None


def extract_hymn_data(url: str, numero: int, collection: str) -> Optional[Dict]:
    """Extract hymn data."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Title
        h1 = soup.find('h1', class_='entry-title') or soup.find('h1')
        title = h1.get_text(strip=True) if h1 else f"Fihirana {numero}"

        # Lyrics
        content_div = soup.find('div', class_='entry-content') or soup.find('article')
        if not content_div:
            return None

        verses = []
        for p in content_div.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 15 and not any(x in text for x in ['Publié', 'Auteur', 'Catégorie', 'Share']):
                verses.append(text)

        paroles = '\n\n'.join(verses)
        if len(paroles) < 50:
            return None

        return {'numero': numero, 'titre': title, 'paroles': paroles, 'collection': collection}
    except:
        return None


def main():
    print("\n" + "="*60)
    print("QUICK IMPORT - First 100 FFPM Hymns")
    print("="*60 + "\n")

    app = create_app()

    with app.app_context():
        imported = 0
        for numero in range(1, 101):
            print(f"[{numero}/100] ", end='', flush=True)

            existing = db.session.query(Fihirana).filter(
                Fihirana.collection == 'FFPM',
                Fihirana.numero == numero
            ).first()

            if existing:
                print(f"✓ #{numero} exists")
                imported += 1
                continue

            url = search_hymn_url(numero, "FFPM")
            if not url:
                print(f"✗ #{numero} not found")
                time.sleep(1)
                continue

            data = extract_hymn_data(url, numero, "FFPM")
            if not data:
                print(f"✗ #{numero} no data")
                time.sleep(1)
                continue

            fihirana = Fihirana(**data)
            db.session.add(fihirana)
            imported += 1

            title_short = data['titre'][:35] + '...' if len(data['titre']) > 35 else data['titre']
            print(f"✓ {title_short}")

            if imported % 10 == 0:
                db.session.commit()

            time.sleep(1.5)  # Faster but still respectful

        db.session.commit()

        print(f"\n{'='*60}")
        print(f"✓ Imported {imported} hymns")
        print(f"{'='*60}\n")

        # Show examples
        examples = db.session.query(Fihirana).filter(Fihirana.collection == 'FFPM').limit(5).all()
        print("Examples:")
        for ex in examples:
            print(f"  #{ex.numero}: {ex.titre}")
        print()


if __name__ == "__main__":
    main()
