"""
Fihirana service for business logic related to hymns data access.
Provides methods to retrieve and search fihirana.
Uses the new verse-based structure (Hira, Tononkira) with fallback to legacy.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from src.models.fihirana import Hira, Tononkira, Sokajy, Fihirana


class FihiranaService:
    """
    Service class for Fihirana data operations.
    Handles retrieving and searching hymns.
    """

    def __init__(self, session: Session):
        """
        Initialize FihiranaService with database session.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        # Check if new structure exists
        self.use_new_structure = session.query(Hira).count() > 0

    def get_all_fihirana(
        self, collection: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get all fihirana, optionally filtered by collection.

        Args:
            collection: Filter by collection (FFPM, Fanampiny, Antema), None for all
            limit: Maximum results to return
            offset: Pagination offset

        Returns:
            List of fihirana dictionaries
        """
        if self.use_new_structure:
            query = self.session.query(Hira).order_by(Hira.collection, Hira.id)

            if collection:
                query = query.filter(Hira.collection == collection)

            hiras = query.limit(limit).offset(offset).all()
            return [hira.to_dict(include_verses=False) for hira in hiras]
        else:
            query = self.session.query(Fihirana).order_by(
                Fihirana.collection, Fihirana.numero
            )

            if collection:
                query = query.filter(Fihirana.collection == collection)

            fihiranas = query.limit(limit).offset(offset).all()
            return [fihirana.to_dict() for fihirana in fihiranas]

    def get_fihirana_by_id(self, fihirana_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific fihirana by ID with all verses.

        Args:
            fihirana_id: ID of the fihirana

        Returns:
            Fihirana dictionary with verses or None if not found
        """
        if self.use_new_structure:
            hira = self.session.query(Hira).filter(Hira.id == fihirana_id).first()
            return hira.to_dict(include_verses=True) if hira else None
        else:
            fihirana = self.session.query(Fihirana).filter(Fihirana.id == fihirana_id).first()
            return fihirana.to_dict() if fihirana else None

    def get_fihirana_by_number(
        self, numero: int, collection: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get a fihirana by its number, optionally within a collection.

        Args:
            numero: Hymn number
            collection: Collection name (optional)

        Returns:
            Fihirana dictionary with verses or None if not found
        """
        if self.use_new_structure:
            query = self.session.query(Hira).filter(Hira.id == numero)

            if collection:
                query = query.filter(Hira.collection == collection)

            hira = query.first()
            return hira.to_dict(include_verses=True) if hira else None
        else:
            query = self.session.query(Fihirana).filter(Fihirana.numero == numero)

            if collection:
                query = query.filter(Fihirana.collection == collection)

            fihirana = query.first()
            return fihirana.to_dict() if fihirana else None

    def search_fihirana(
        self,
        query_text: str,
        collection: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Search fihirana by text (title or lyrics).

        Args:
            query_text: Search query
            collection: Filter by collection (optional)
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of matching fihirana dictionaries
        """
        search_term = f"%{query_text}%"

        if self.use_new_structure:
            # Search in Hira titles and Tononkira verses
            hira_ids_from_verses = (
                self.session.query(Tononkira.hira_id)
                .filter(Tononkira.tononkira.ilike(search_term))
                .distinct()
                .subquery()
            )

            query = self.session.query(Hira).filter(
                or_(
                    Hira.lohateny.ilike(search_term),
                    Hira.id.in_(hira_ids_from_verses)
                )
            )

            if collection:
                query = query.filter(Hira.collection == collection)

            hiras = (
                query.order_by(Hira.collection, Hira.id)
                .limit(limit)
                .offset(offset)
                .all()
            )

            return [hira.to_dict(include_verses=False) for hira in hiras]
        else:
            query = self.session.query(Fihirana).filter(
                (Fihirana.titre.ilike(search_term)) | (Fihirana.paroles.ilike(search_term))
            )

            if collection:
                query = query.filter(Fihirana.collection == collection)

            fihiranas = (
                query.order_by(Fihirana.collection, Fihirana.numero)
                .limit(limit)
                .offset(offset)
                .all()
            )

            return [fihirana.to_dict() for fihirana in fihiranas]

    def count_search_results(
        self, query_text: str, collection: Optional[str] = None
    ) -> int:
        """
        Count total search results.

        Args:
            query_text: Search query
            collection: Filter by collection (optional)

        Returns:
            Total count of matching results
        """
        search_term = f"%{query_text}%"

        if self.use_new_structure:
            hira_ids_from_verses = (
                self.session.query(Tononkira.hira_id)
                .filter(Tononkira.tononkira.ilike(search_term))
                .distinct()
                .subquery()
            )

            query = self.session.query(func.count(Hira.id)).filter(
                or_(
                    Hira.lohateny.ilike(search_term),
                    Hira.id.in_(hira_ids_from_verses)
                )
            )

            if collection:
                query = query.filter(Hira.collection == collection)

            return query.scalar()
        else:
            query = self.session.query(func.count(Fihirana.id)).filter(
                (Fihirana.titre.ilike(search_term)) | (Fihirana.paroles.ilike(search_term))
            )

            if collection:
                query = query.filter(Fihirana.collection == collection)

            return query.scalar()

    def count_by_collection(self, collection: Optional[str] = None) -> int:
        """
        Count fihirana in a collection.

        Args:
            collection: Collection name, None for total

        Returns:
            Count of fihirana
        """
        if self.use_new_structure:
            query = self.session.query(func.count(Hira.id))

            if collection:
                query = query.filter(Hira.collection == collection)

            return query.scalar()
        else:
            query = self.session.query(func.count(Fihirana.id))

            if collection:
                query = query.filter(Fihirana.collection == collection)

            return query.scalar()
