"""
Fihirana (Hymn) database models.
Defines the Fihirana table for storing Malagasy hymns from FFPM, Fanampiny, and Antema collections.
"""
from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.dialects.postgresql import TSVECTOR
from src.app import db


class Fihirana(db.Model):
    """
    Fihirana model representing a hymn.

    Attributes:
        id: Primary key
        numero: Hymn number within its collection
        titre: Hymn title
        paroles: Full lyrics text
        collection: Collection name (FFPM, Fanampiny, Antema)
        search_vector: Full-text search vector for Malagasy text
    """
    __tablename__ = 'fihirana'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False)
    titre = Column(String(255), nullable=False)
    paroles = Column(Text, nullable=False)
    collection = Column(String(50), nullable=False, index=True)  # FFPM, Fanampiny, Antema

    # Full-text search vector
    search_vector = Column(TSVECTOR)

    # Indexes for performance
    __table_args__ = (
        Index('idx_fihirana_numero', 'numero'),
        Index('idx_fihirana_collection', 'collection'),
        Index('idx_fihirana_search', 'search_vector', postgresql_using='gin'),
        Index('idx_fihirana_collection_numero', 'collection', 'numero'),
    )

    def __repr__(self):
        return f"<Fihirana {self.collection} #{self.numero}: {self.titre}>"

    def to_dict(self) -> dict:
        """
        Convert fihirana to dictionary representation.

        Returns:
            Dictionary with fihirana data
        """
        return {
            'id': self.id,
            'numero': self.numero,
            'titre': self.titre,
            'paroles': self.paroles,
            'collection': self.collection,
        }
