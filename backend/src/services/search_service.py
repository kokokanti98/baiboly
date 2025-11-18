"""
Search service for full-text search in Bible verses.
Uses PostgreSQL full-text search with tsvector and GIN indexes.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from src.models.bible import Verset, Chapitre, Livre


class SearchService:
    """
    Service class for full-text search operations on Bible verses.
    """

    def __init__(self, session: Session):
        """
        Initialize SearchService with database session.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session

    def search_versets(
        self,
        query: str,
        livre_id: Optional[int] = None,
        testament: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Search for verses by text content using PostgreSQL full-text search.

        Args:
            query: Search query string
            livre_id: Optional filter by specific book ID
            testament: Optional filter by testament ("AT" or "NT")
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of verset dictionaries with livre and chapitre references
        """
        # Build base query with joins for livre and chapitre info
        search_query = (
            self.session.query(Verset)
            .join(Chapitre)
            .join(Livre)
            .options(joinedload(Verset.chapitre).joinedload(Chapitre.livre))
        )

        # Apply filters
        if livre_id:
            search_query = search_query.filter(Livre.id == livre_id)

        if testament:
            search_query = search_query.filter(Livre.testament == testament)

        # Full-text search using tsvector
        # Use to_tsquery for PostgreSQL FTS or fallback to ILIKE for simple search
        try:
            # PostgreSQL full-text search
            ts_query = func.plainto_tsquery('simple', query)
            search_query = search_query.filter(
                Verset.texte_search_vector.op('@@')(ts_query)
            )
        except Exception:
            # Fallback to case-insensitive LIKE search
            search_pattern = f"%{query}%"
            search_query = search_query.filter(
                func.lower(Verset.texte).like(func.lower(search_pattern))
            )

        # Order by relevance (verse order) and apply pagination
        search_query = (
            search_query.order_by(Livre.ordre, Chapitre.numero, Verset.numero)
            .limit(limit)
            .offset(offset)
        )

        # Execute query and return results
        versets = search_query.all()
        return [verset.to_dict(include_references=True) for verset in versets]

    def search_versets_simple(
        self,
        query: str,
        livre_id: Optional[int] = None,
        testament: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Simple case-insensitive search using ILIKE.
        Used as fallback when PostgreSQL FTS is not available.

        Args:
            query: Search query string
            livre_id: Optional filter by specific book ID
            testament: Optional filter by testament ("AT" or "NT")
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of verset dictionaries with livre and chapitre references
        """
        # Build query with case-insensitive search
        search_pattern = f"%{query}%"

        search_query = (
            self.session.query(Verset)
            .join(Chapitre)
            .join(Livre)
            .options(joinedload(Verset.chapitre).joinedload(Chapitre.livre))
            .filter(Verset.texte.ilike(search_pattern))
        )

        # Apply filters
        if livre_id:
            search_query = search_query.filter(Livre.id == livre_id)

        if testament:
            search_query = search_query.filter(Livre.testament == testament)

        # Order and paginate
        search_query = (
            search_query.order_by(Livre.ordre, Chapitre.numero, Verset.numero)
            .limit(limit)
            .offset(offset)
        )

        versets = search_query.all()
        return [verset.to_dict(include_references=True) for verset in versets]

    def search_versets_multi_word(
        self,
        query: str,
        livre_id: Optional[int] = None,
        testament: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Search for verses containing multiple words (AND logic).
        Each word must appear in the verse.

        Args:
            query: Search query with multiple words
            livre_id: Optional filter by specific book ID
            testament: Optional filter by testament
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of verset dictionaries
        """
        words = query.lower().split()

        search_query = (
            self.session.query(Verset)
            .join(Chapitre)
            .join(Livre)
            .options(joinedload(Verset.chapitre).joinedload(Chapitre.livre))
        )

        # Apply word filters (all words must be present)
        for word in words:
            search_query = search_query.filter(
                func.lower(Verset.texte).like(f"%{word}%")
            )

        # Apply optional filters
        if livre_id:
            search_query = search_query.filter(Livre.id == livre_id)

        if testament:
            search_query = search_query.filter(Livre.testament == testament)

        # Order and paginate
        search_query = (
            search_query.order_by(Livre.ordre, Chapitre.numero, Verset.numero)
            .limit(limit)
            .offset(offset)
        )

        versets = search_query.all()
        return [verset.to_dict(include_references=True) for verset in versets]

    def count_search_results(
        self,
        query: str,
        livre_id: Optional[int] = None,
        testament: Optional[str] = None,
    ) -> int:
        """
        Count total number of search results (for pagination).

        Args:
            query: Search query string
            livre_id: Optional filter by specific book ID
            testament: Optional filter by testament

        Returns:
            Total count of matching verses
        """
        search_pattern = f"%{query}%"

        count_query = (
            self.session.query(func.count(Verset.id))
            .join(Chapitre)
            .join(Livre)
            .filter(Verset.texte.ilike(search_pattern))
        )

        if livre_id:
            count_query = count_query.filter(Livre.id == livre_id)

        if testament:
            count_query = count_query.filter(Livre.testament == testament)

        return count_query.scalar()
