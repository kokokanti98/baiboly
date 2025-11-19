"""
Fihirana (Hymn) database models.
Defines tables for storing Malagasy hymns with verse-by-verse structure.
Based on the structure from https://github.com/Rohan29-AN/Fihirana-FFPM
"""
from sqlalchemy import Column, Integer, String, Text, Index, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import relationship
from src.app import db


class Sokajy(db.Model):
    """
    Sokajy (Category) model for hymn categories.

    Attributes:
        id: Primary key
        anarana: Category name
        hira: Relationship to hymns in this category
    """
    __tablename__ = 'sokajy'

    id = Column(Integer, primary_key=True)
    anarana = Column(String(255), nullable=False)

    # Relationships
    hira = relationship('Hira', back_populates='sokajy', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Sokajy {self.id}: {self.anarana}>"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'anarana': self.anarana,
        }


class Hira(db.Model):
    """
    Hira (Hymn) model representing a complete hymn.

    Attributes:
        id: Primary key (unique ID with offset per collection)
        numero_affiche: Display number (actual hymn number shown to users)
        sokajy_id: Foreign key to category
        lohateny: Hymn title (formatted with prefix for ANTEMA/FANAMPINY)
        isa_andininy: Number of verses
        mpanoratra: Author/composer
        collection: Collection name (FFPM, Fanampiny, etc.)
        sokajy: Relationship to category
        tononkira: Relationship to verses
    """
    __tablename__ = 'hira'

    id = Column(Integer, primary_key=True)  # Unique ID with offset
    numero_affiche = Column(Integer, nullable=False, index=True)  # Display number
    sokajy_id = Column(Integer, ForeignKey('sokajy.id'), nullable=True)
    lohateny = Column(String(255), nullable=False)  # Title with prefix
    isa_andininy = Column(Integer, nullable=False)  # Number of verses
    mpanoratra = Column(String(255), nullable=True)  # Author
    collection = Column(String(50), nullable=False, default='FFPM', index=True)

    # Relationships
    sokajy = relationship('Sokajy', back_populates='hira')
    tononkira = relationship('Tononkira', back_populates='hira',
                            order_by='Tononkira.andininy',
                            cascade='all, delete-orphan')

    # Indexes
    __table_args__ = (
        Index('idx_hira_collection', 'collection'),
        Index('idx_hira_sokajy', 'sokajy_id'),
    )

    def __repr__(self):
        return f"<Hira #{self.id}: {self.lohateny}>"

    def to_dict(self, include_verses=True) -> dict:
        """
        Convert hira to dictionary.

        Args:
            include_verses: Whether to include verse details

        Returns:
            Dictionary with hymn data
        """
        result = {
            'id': self.id,
            'numero': self.numero_affiche,  # Display number
            'numero_affiche': self.numero_affiche,  # Explicit field
            'lohateny': self.lohateny,
            'titre': self.lohateny,  # For compatibility
            'isa_andininy': self.isa_andininy,
            'mpanoratra': self.mpanoratra,
            'collection': self.collection,
        }

        if self.sokajy:
            result['sokajy'] = self.sokajy.to_dict()

        if include_verses and self.tononkira:
            result['tononkira'] = [v.to_dict() for v in self.tononkira]
            # Also include full formatted text
            result['paroles'] = self.get_formatted_paroles()

        return result

    def get_formatted_paroles(self) -> str:
        """
        Get formatted lyrics with verse numbers.

        Returns:
            Formatted lyrics string with verse numbers
        """
        if not self.tononkira:
            return ""

        verses = []
        refrain_text = None

        for verse in self.tononkira:
            if verse.fiverenany:
                # This is a refrain, save it
                refrain_text = verse.tononkira
            else:
                # Regular verse - add with number
                verses.append(f"{verse.andininy}. {verse.tononkira}")

                # Add refrain after each verse if it exists
                if refrain_text:
                    verses.append(f"\nFiverenana:\n{refrain_text}")

        return "\n\n".join(verses)


class Tononkira(db.Model):
    """
    Tononkira (Verse) model representing a hymn verse or refrain.

    Attributes:
        id: Primary key
        hira_id: Foreign key to hymn
        andininy: Verse number
        tononkira: Verse lyrics text
        fiverenany: Whether this is a refrain (True) or verse (False)
        search_vector: Full-text search vector
        hira: Relationship to hymn
    """
    __tablename__ = 'tononkira'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hira_id = Column(Integer, ForeignKey('hira.id'), nullable=False)
    andininy = Column(Integer, nullable=False)  # Verse number
    tononkira = Column(Text, nullable=False)  # Verse text
    fiverenany = Column(Boolean, default=False)  # Is this a refrain?

    # Full-text search vector
    search_vector = Column(TSVECTOR)

    # Relationships
    hira = relationship('Hira', back_populates='tononkira')

    # Indexes
    __table_args__ = (
        Index('idx_tononkira_hira', 'hira_id'),
        Index('idx_tononkira_search', 'search_vector', postgresql_using='gin'),
    )

    def __repr__(self):
        verse_type = "Fiverenana" if self.fiverenany else f"Andininy {self.andininy}"
        return f"<Tononkira Hira#{self.hira_id} {verse_type}>"

    def to_dict(self) -> dict:
        """
        Convert verse to dictionary.

        Returns:
            Dictionary with verse data
        """
        return {
            'id': self.id,
            'hira_id': self.hira_id,
            'andininy': self.andininy,
            'tononkira': self.tononkira,
            'fiverenany': self.fiverenany,
        }


# Legacy Fihirana model for backward compatibility
# This can be removed after full migration
class Fihirana(db.Model):
    """
    Legacy Fihirana model (flat structure).
    Kept for backward compatibility during migration.
    """
    __tablename__ = 'fihirana_legacy'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False)
    titre = Column(String(255), nullable=False)
    paroles = Column(Text, nullable=False)
    collection = Column(String(50), nullable=False, index=True)
    search_vector = Column(TSVECTOR)

    __table_args__ = (
        Index('idx_fihirana_legacy_numero', 'numero'),
        Index('idx_fihirana_legacy_collection', 'collection'),
        Index('idx_fihirana_legacy_search', 'search_vector', postgresql_using='gin'),
    )

    def __repr__(self):
        return f"<Fihirana {self.collection} #{self.numero}: {self.titre}>"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'numero': self.numero,
            'titre': self.titre,
            'paroles': self.paroles,
            'collection': self.collection,
        }
