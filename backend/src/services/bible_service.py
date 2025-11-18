"""
Bible service for business logic related to Bible data access.
Provides methods to retrieve livres, chapitres, and versets.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from src.models.bible import Livre, Chapitre, Verset


class BibleService:
    """
    Service class for Bible data operations.
    Handles retrieving books, chapters, and verses.
    """

    def __init__(self, session: Session):
        """
        Initialize BibleService with database session.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session

    def get_all_livres(self, testament: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all Bible books, optionally filtered by testament.

        Args:
            testament: Filter by testament ("AT" or "NT"), None for all

        Returns:
            List of livre dictionaries
        """
        query = self.session.query(Livre).order_by(Livre.ordre)

        if testament:
            query = query.filter(Livre.testament == testament)

        livres = query.all()
        return [livre.to_dict() for livre in livres]

    def get_livre_by_id(self, livre_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific livre by ID.

        Args:
            livre_id: ID of the livre

        Returns:
            Livre dictionary or None if not found
        """
        livre = self.session.query(Livre).filter(Livre.id == livre_id).first()
        return livre.to_dict() if livre else None

    def get_livre_by_name(self, nom: str) -> Optional[Dict[str, Any]]:
        """
        Get a livre by its name.

        Args:
            nom: Name of the livre (e.g., "Genesisy")

        Returns:
            Livre dictionary or None if not found
        """
        livre = self.session.query(Livre).filter(Livre.nom == nom).first()
        return livre.to_dict() if livre else None

    def get_livre_by_abbrev(self, abbrev: str) -> Optional[Dict[str, Any]]:
        """
        Get a livre by its abbreviation.

        Args:
            abbrev: Abbreviation (e.g., "Gen")

        Returns:
            Livre dictionary or None if not found
        """
        livre = self.session.query(Livre).filter(Livre.abbrev == abbrev).first()
        return livre.to_dict() if livre else None

    def get_chapitres_by_livre(self, livre_id: int) -> List[Dict[str, Any]]:
        """
        Get all chapters for a specific book.

        Args:
            livre_id: ID of the livre

        Returns:
            List of chapitre dictionaries
        """
        chapitres = (
            self.session.query(Chapitre)
            .filter(Chapitre.livre_id == livre_id)
            .order_by(Chapitre.numero)
            .all()
        )
        return [chapitre.to_dict() for chapitre in chapitres]

    def get_chapitre_by_id(self, chapitre_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific chapter by ID.

        Args:
            chapitre_id: ID of the chapitre

        Returns:
            Chapitre dictionary or None if not found
        """
        chapitre = self.session.query(Chapitre).filter(Chapitre.id == chapitre_id).first()
        return chapitre.to_dict() if chapitre else None

    def get_versets_by_chapitre(self, chapitre_id: int) -> List[Dict[str, Any]]:
        """
        Get all verses for a specific chapter.

        Args:
            chapitre_id: ID of the chapitre

        Returns:
            List of verset dictionaries
        """
        versets = (
            self.session.query(Verset)
            .filter(Verset.chapitre_id == chapitre_id)
            .order_by(Verset.numero)
            .all()
        )
        return [verset.to_dict() for verset in versets]

    def get_verset_by_id(self, verset_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific verse by ID.

        Args:
            verset_id: ID of the verset

        Returns:
            Verset dictionary or None if not found
        """
        verset = self.session.query(Verset).filter(Verset.id == verset_id).first()
        return verset.to_dict() if verset else None

    def get_verset_by_reference(
        self, livre_abbrev: str, chapitre_numero: int, verset_numero: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific verse by Bible reference (e.g., Gen 1:1).

        Args:
            livre_abbrev: Book abbreviation (e.g., "Gen")
            chapitre_numero: Chapter number
            verset_numero: Verse number

        Returns:
            Verset dictionary with livre and chapitre info, or None if not found
        """
        verset = (
            self.session.query(Verset)
            .join(Chapitre)
            .join(Livre)
            .filter(
                Livre.abbrev == livre_abbrev,
                Chapitre.numero == chapitre_numero,
                Verset.numero == verset_numero,
            )
            .options(joinedload(Verset.chapitre).joinedload(Chapitre.livre))
            .first()
        )

        return verset.to_dict(include_references=True) if verset else None

    def get_versets_range(
        self,
        livre_abbrev: str,
        chapitre_numero: int,
        verset_debut: int,
        verset_fin: int,
    ) -> List[Dict[str, Any]]:
        """
        Get a range of verses (e.g., Gen 1:1-3).

        Args:
            livre_abbrev: Book abbreviation (e.g., "Gen")
            chapitre_numero: Chapter number
            verset_debut: Starting verse number
            verset_fin: Ending verse number

        Returns:
            List of verset dictionaries with references
        """
        versets = (
            self.session.query(Verset)
            .join(Chapitre)
            .join(Livre)
            .filter(
                Livre.abbrev == livre_abbrev,
                Chapitre.numero == chapitre_numero,
                Verset.numero >= verset_debut,
                Verset.numero <= verset_fin,
            )
            .options(joinedload(Verset.chapitre).joinedload(Chapitre.livre))
            .order_by(Verset.numero)
            .all()
        )

        return [verset.to_dict(include_references=True) for verset in versets]
