"""
SQLAlchemy models for Bible data (Livre, Chapitre, Verset).
Constitutional requirement: PostgreSQL with full-text search support.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TSVECTOR
from src.app import db


class Livre(db.Model):
    """
    Bible book model (Livre = Book in French/Malagasy).
    Represents a book of the Bible (e.g., Genesis, Exodus).
    """
    __tablename__ = 'livre'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False, unique=True)  # Book name in Malagasy
    abbrev = Column(String(10), nullable=False, unique=True)  # Abbreviation (e.g., "Gen")
    testament = Column(String(2), nullable=False)  # "AT" (Old) or "NT" (New)
    ordre = Column(Integer, nullable=False)  # Order in Bible (1-66)

    # Relationships
    chapitres = relationship('Chapitre', back_populates='livre', cascade='all, delete-orphan')

    # Constraints
    __table_args__ = (
        UniqueConstraint('testament', 'ordre', name='uq_livre_testament_ordre'),
        Index('ix_livre_testament', 'testament'),
        Index('ix_livre_ordre', 'ordre'),
    )

    def __repr__(self):
        return f"<Livre {self.abbrev}: {self.nom}>"

    def to_dict(self):
        """Serialize to dictionary for JSON responses."""
        return {
            'id': self.id,
            'nom': self.nom,
            'abbrev': self.abbrev,
            'testament': self.testament,
            'ordre': self.ordre,
        }


class Chapitre(db.Model):
    """
    Bible chapter model (Chapitre = Chapter in French).
    Represents a chapter within a book.
    """
    __tablename__ = 'chapitre'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False)  # Chapter number
    livre_id = Column(Integer, ForeignKey('livre.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    livre = relationship('Livre', back_populates='chapitres')
    versets = relationship('Verset', back_populates='chapitre', cascade='all, delete-orphan')

    # Constraints
    __table_args__ = (
        UniqueConstraint('livre_id', 'numero', name='uq_chapitre_livre_numero'),
        Index('ix_chapitre_livre_id', 'livre_id'),
    )

    def __repr__(self):
        return f"<Chapitre {self.livre.abbrev if self.livre else '?'} {self.numero}>"

    def to_dict(self):
        """Serialize to dictionary for JSON responses."""
        return {
            'id': self.id,
            'numero': self.numero,
            'livre_id': self.livre_id,
        }


class Verset(db.Model):
    """
    Bible verse model (Verset = Verse in French).
    Represents a single verse within a chapter.
    Includes full-text search support via tsvector column.
    """
    __tablename__ = 'verset'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False)  # Verse number
    texte = Column(Text, nullable=False)  # Verse text in Malagasy
    chapitre_id = Column(Integer, ForeignKey('chapitre.id', ondelete='CASCADE'), nullable=False)

    # Full-text search vector (populated by trigger or application)
    texte_search_vector = Column(TSVECTOR)

    # Relationships
    chapitre = relationship('Chapitre', back_populates='versets')

    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint('chapitre_id', 'numero', name='uq_verset_chapitre_numero'),
        Index('ix_verset_chapitre_id', 'chapitre_id'),
        Index('ix_verset_texte_search', 'texte_search_vector', postgresql_using='gin'),
    )

    def __repr__(self):
        ref = ""
        if self.chapitre and self.chapitre.livre:
            ref = f"{self.chapitre.livre.abbrev} {self.chapitre.numero}:{self.numero}"
        else:
            ref = f"Verset {self.numero}"
        return f"<Verset {ref}>"

    def to_dict(self, include_references=False):
        """
        Serialize to dictionary for JSON responses.

        Args:
            include_references: If True, include livre and chapitre info
        """
        result = {
            'id': self.id,
            'numero': self.numero,
            'texte': self.texte,
            'chapitre_id': self.chapitre_id,
        }

        if include_references and self.chapitre:
            result['chapitre'] = {
                'id': self.chapitre.id,
                'numero': self.chapitre.numero,
            }
            if self.chapitre.livre:
                result['livre'] = {
                    'id': self.chapitre.livre.id,
                    'nom': self.chapitre.livre.nom,
                    'abbrev': self.chapitre.livre.abbrev,
                    'testament': self.chapitre.livre.testament,
                }

        return result
