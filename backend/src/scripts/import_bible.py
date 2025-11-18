"""
Script to import Bible data from GitHub JSON files.
Downloads data from: https://github.com/RaveloMevaSoavina/baiboly-json
"""
import os
import json
import requests
from sqlalchemy import func
from src.app import create_app, db
from src.models.bible import Livre, Chapitre, Verset
from src.scripts.import_all_bible_books import get_all_books

# GitHub raw content base URL
GITHUB_BASE_URL = "https://raw.githubusercontent.com/RaveloMevaSoavina/baiboly-json/master"

# Get all 66 Bible books
OLD_TESTAMENT_BOOKS, NEW_TESTAMENT_BOOKS = get_all_books()


def download_book_data(testament_folder, filename):
    """
    Download book data from GitHub.

    Args:
        testament_folder: "Testameta taloha" or "Testameta vaovao"
        filename: JSON filename

    Returns:
        dict: Book data or None if error
    """
    url = f"{GITHUB_BASE_URL}/{testament_folder}/{filename}"
    print(f"Downloading {filename} from {url}...")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return None


def import_book(book_config, testament):
    """
    Import a single book with its chapters and verses.

    Args:
        book_config: Book configuration dict
        testament: "AT" or "NT"
    """
    # Determine testament folder
    testament_folder = "Testameta taloha" if testament == "AT" else "Testameta vaovao"

    # Download book data
    book_data = download_book_data(testament_folder, book_config["file"])
    if not book_data:
        print(f"Skipping {book_config['nom']} - download failed")
        return

    # Check if book already exists
    existing_livre = Livre.query.filter_by(nom=book_config["nom"]).first()
    if existing_livre:
        print(f"Book {book_config['nom']} already exists, skipping...")
        return

    # Create Livre
    livre = Livre(
        nom=book_config["nom"],
        abbrev=book_config["abbrev"],
        testament=testament,
        ordre=book_config["ordre"]
    )
    db.session.add(livre)
    db.session.flush()  # Get livre.id

    print(f"Importing {livre.nom} ({livre.abbrev})...")

    # Import chapters and verses
    # Expected JSON structure: {"1": {"1": "text...", "2": "text..."}, "2": {...}}
    # Keys are chapter numbers (as strings), values are dicts of verse number -> text

    verse_count = 0
    for chapitre_numero_str, verses_dict in book_data.items():
        try:
            chapitre_numero = int(chapitre_numero_str)
        except ValueError:
            print(f"  - Skipping invalid chapter key: {chapitre_numero_str}")
            continue

        # Create Chapitre
        chapitre = Chapitre(
            numero=chapitre_numero,
            livre_id=livre.id
        )
        db.session.add(chapitre)
        db.session.flush()  # Get chapitre.id

        # Import verses
        for verset_numero_str, texte in verses_dict.items():
            try:
                verset_numero = int(verset_numero_str)
            except ValueError:
                print(f"  - Skipping invalid verse key: {verset_numero_str}")
                continue

            # Create Verset
            verset = Verset(
                numero=verset_numero,
                texte=texte,
                chapitre_id=chapitre.id
            )
            db.session.add(verset)
            verse_count += 1

        print(f"  - Chapter {chapitre_numero}: {len(verses_dict)} verses")

    db.session.commit()
    print(f"✓ Imported {livre.nom} successfully")


def update_search_vectors():
    """
    Update tsvector columns for full-text search.
    """
    print("\nUpdating search vectors for full-text search...")

    # Update all verses with search vectors
    db.session.execute(
        Verset.__table__.update().values(
            texte_search_vector=func.to_tsvector('simple', Verset.texte)
        )
    )
    db.session.commit()
    print("✓ Search vectors updated")


def import_all_books():
    """Import all Bible books from GitHub."""
    print("=" * 60)
    print("IMPORTING BIBLE DATA FROM GITHUB")
    print("=" * 60)

    # Import Old Testament
    print("\n--- OLD TESTAMENT (Testameta Taloha) ---")
    for book in OLD_TESTAMENT_BOOKS:
        try:
            import_book(book, "AT")
        except Exception as e:
            print(f"Error importing {book['nom']}: {e}")
            db.session.rollback()

    # Import New Testament
    print("\n--- NEW TESTAMENT (Testameta Vaovao) ---")
    for book in NEW_TESTAMENT_BOOKS:
        try:
            import_book(book, "NT")
        except Exception as e:
            print(f"Error importing {book['nom']}: {e}")
            db.session.rollback()

    # Update search vectors
    update_search_vectors()

    # Print summary
    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    total_livres = Livre.query.count()
    total_chapitres = Chapitre.query.count()
    total_versets = Verset.query.count()

    print(f"Total Books (Livres): {total_livres}")
    print(f"Total Chapters (Chapitres): {total_chapitres}")
    print(f"Total Verses (Versets): {total_versets}")
    print("=" * 60)


if __name__ == "__main__":
    # Create Flask app context
    app = create_app()
    with app.app_context():
        import_all_books()
