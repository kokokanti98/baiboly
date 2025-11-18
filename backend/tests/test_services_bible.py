"""
TDD Tests for Bible services (BibleService, SearchService).
These tests must FAIL initially, then pass after implementation.
Constitutional requirement: TDD workflow enforced.
"""
import pytest
from src.services.bible_service import BibleService
from src.services.search_service import SearchService
from src.models.bible import Livre, Chapitre, Verset


@pytest.mark.unit
@pytest.mark.bible
class TestBibleService:
    """Test suite for BibleService."""

    def test_get_all_livres(self, session):
        """Test getting all Bible books."""
        # Create sample data
        livre1 = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        livre2 = Livre(nom="Eksodosy", abbrev="Exo", testament="AT", ordre=2)
        session.add_all([livre1, livre2])
        session.commit()

        service = BibleService(session)
        livres = service.get_all_livres()

        assert len(livres) == 2
        assert livres[0]['nom'] == "Genesisy"
        assert livres[1]['nom'] == "Eksodosy"

    def test_get_all_livres_ordered_by_ordre(self, session):
        """Test that livres are returned in correct order."""
        livre2 = Livre(nom="Eksodosy", abbrev="Exo", testament="AT", ordre=2)
        livre1 = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add_all([livre2, livre1])  # Add in wrong order
        session.commit()

        service = BibleService(session)
        livres = service.get_all_livres()

        assert livres[0]['nom'] == "Genesisy"  # Should be first
        assert livres[1]['nom'] == "Eksodosy"  # Should be second

    def test_get_all_livres_by_testament(self, session):
        """Test filtering livres by testament."""
        livre_at = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        livre_nt = Livre(nom="Matio", abbrev="Mat", testament="NT", ordre=40)
        session.add_all([livre_at, livre_nt])
        session.commit()

        service = BibleService(session)
        livres_at = service.get_all_livres(testament="AT")
        livres_nt = service.get_all_livres(testament="NT")

        assert len(livres_at) == 1
        assert livres_at[0]['nom'] == "Genesisy"
        assert len(livres_nt) == 1
        assert livres_nt[0]['nom'] == "Matio"

    def test_get_livre_by_id(self, session):
        """Test getting a specific livre by ID."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        service = BibleService(session)
        result = service.get_livre_by_id(livre.id)

        assert result is not None
        assert result['nom'] == "Genesisy"
        assert result['id'] == livre.id

    def test_get_livre_by_id_not_found(self, session):
        """Test getting a non-existent livre returns None."""
        service = BibleService(session)
        result = service.get_livre_by_id(999)

        assert result is None

    def test_get_livre_by_name(self, session):
        """Test getting a livre by name."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        service = BibleService(session)
        result = service.get_livre_by_name("Genesisy")

        assert result is not None
        assert result['nom'] == "Genesisy"

    def test_get_livre_by_abbrev(self, session):
        """Test getting a livre by abbreviation."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        service = BibleService(session)
        result = service.get_livre_by_abbrev("Gen")

        assert result is not None
        assert result['nom'] == "Genesisy"
        assert result['abbrev'] == "Gen"

    def test_get_chapitres_by_livre(self, session):
        """Test getting all chapters for a book."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre1 = Chapitre(numero=1, livre_id=livre.id)
        chapitre2 = Chapitre(numero=2, livre_id=livre.id)
        session.add_all([chapitre1, chapitre2])
        session.commit()

        service = BibleService(session)
        chapitres = service.get_chapitres_by_livre(livre.id)

        assert len(chapitres) == 2
        assert chapitres[0]['numero'] == 1
        assert chapitres[1]['numero'] == 2

    def test_get_chapitre_by_id(self, session):
        """Test getting a specific chapter by ID."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        service = BibleService(session)
        result = service.get_chapitre_by_id(chapitre.id)

        assert result is not None
        assert result['numero'] == 1

    def test_get_versets_by_chapitre(self, session):
        """Test getting all verses for a chapter."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset1 = Verset(numero=1, texte="Premier verset", chapitre_id=chapitre.id)
        verset2 = Verset(numero=2, texte="Deuxième verset", chapitre_id=chapitre.id)
        session.add_all([verset1, verset2])
        session.commit()

        service = BibleService(session)
        versets = service.get_versets_by_chapitre(chapitre.id)

        assert len(versets) == 2
        assert versets[0]['numero'] == 1
        assert versets[1]['numero'] == 2

    def test_get_verset_by_id(self, session):
        """Test getting a specific verse by ID."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset = Verset(numero=1, texte="Premier verset", chapitre_id=chapitre.id)
        session.add(verset)
        session.commit()

        service = BibleService(session)
        result = service.get_verset_by_id(verset.id)

        assert result is not None
        assert result['numero'] == 1
        assert result['texte'] == "Premier verset"

    def test_get_verset_by_reference(self, session):
        """Test getting a verse by Bible reference (e.g., Gen 1:1)."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset = Verset(
            numero=1,
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
            chapitre_id=chapitre.id
        )
        session.add(verset)
        session.commit()

        service = BibleService(session)
        result = service.get_verset_by_reference("Gen", 1, 1)

        assert result is not None
        assert result['numero'] == 1
        assert "Andriamanitra" in result['texte']

    def test_get_verset_by_reference_not_found(self, session):
        """Test getting a non-existent verse reference returns None."""
        service = BibleService(session)
        result = service.get_verset_by_reference("Gen", 1, 999)

        assert result is None

    def test_get_versets_range(self, session):
        """Test getting a range of verses (e.g., Gen 1:1-3)."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset1 = Verset(numero=1, texte="Verset 1", chapitre_id=chapitre.id)
        verset2 = Verset(numero=2, texte="Verset 2", chapitre_id=chapitre.id)
        verset3 = Verset(numero=3, texte="Verset 3", chapitre_id=chapitre.id)
        session.add_all([verset1, verset2, verset3])
        session.commit()

        service = BibleService(session)
        result = service.get_versets_range("Gen", 1, 1, 3)

        assert len(result) == 3
        assert result[0]['numero'] == 1
        assert result[2]['numero'] == 3


@pytest.mark.unit
@pytest.mark.bible
@pytest.mark.search
class TestSearchService:
    """Test suite for SearchService (full-text search)."""

    def test_search_versets_by_text(self, session):
        """Test searching verses by text content."""
        # Setup test data
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset1 = Verset(
            numero=1,
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
            chapitre_id=chapitre.id
        )
        verset2 = Verset(
            numero=2,
            texte="Ny tany dia tsy nisy endrika sady foana.",
            chapitre_id=chapitre.id
        )
        session.add_all([verset1, verset2])
        session.commit()

        service = SearchService(session)
        results = service.search_versets("Andriamanitra")

        assert len(results) >= 1
        assert "Andriamanitra" in results[0]['texte']

    def test_search_versets_case_insensitive(self, session):
        """Test that search is case-insensitive."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset = Verset(
            numero=1,
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
            chapitre_id=chapitre.id
        )
        session.add(verset)
        session.commit()

        service = SearchService(session)
        results_lower = service.search_versets("andriamanitra")
        results_upper = service.search_versets("ANDRIAMANITRA")

        assert len(results_lower) >= 1
        assert len(results_upper) >= 1

    def test_search_versets_partial_word(self, session):
        """Test searching with partial words."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset = Verset(
            numero=1,
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
            chapitre_id=chapitre.id
        )
        session.add(verset)
        session.commit()

        service = SearchService(session)
        results = service.search_versets("lanit")  # Partial word

        assert len(results) >= 1

    def test_search_versets_multiple_words(self, session):
        """Test searching with multiple words."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset = Verset(
            numero=1,
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
            chapitre_id=chapitre.id
        )
        session.add(verset)
        session.commit()

        service = SearchService(session)
        results = service.search_versets("Andriamanitra lanitra")

        assert len(results) >= 1

    def test_search_versets_no_results(self, session):
        """Test search returns empty list when no matches."""
        service = SearchService(session)
        results = service.search_versets("nonexistentword12345")

        assert len(results) == 0

    def test_search_versets_with_limit(self, session):
        """Test search with result limit."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        # Create multiple verses with same word
        for i in range(1, 11):
            verset = Verset(
                numero=i,
                texte=f"Verset {i} avec Andriamanitra",
                chapitre_id=chapitre.id
            )
            session.add(verset)
        session.commit()

        service = SearchService(session)
        results = service.search_versets("Andriamanitra", limit=5)

        assert len(results) == 5

    def test_search_versets_with_offset(self, session):
        """Test search with pagination offset."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        # Create multiple verses
        for i in range(1, 11):
            verset = Verset(
                numero=i,
                texte=f"Verset {i} avec Andriamanitra",
                chapitre_id=chapitre.id
            )
            session.add(verset)
        session.commit()

        service = SearchService(session)
        results_page1 = service.search_versets("Andriamanitra", limit=5, offset=0)
        results_page2 = service.search_versets("Andriamanitra", limit=5, offset=5)

        assert len(results_page1) == 5
        assert len(results_page2) == 5
        assert results_page1[0]['id'] != results_page2[0]['id']

    def test_search_versets_filter_by_livre(self, session):
        """Test searching verses filtered by specific book."""
        livre1 = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        livre2 = Livre(nom="Eksodosy", abbrev="Exo", testament="AT", ordre=2)
        session.add_all([livre1, livre2])
        session.commit()

        chapitre1 = Chapitre(numero=1, livre_id=livre1.id)
        chapitre2 = Chapitre(numero=1, livre_id=livre2.id)
        session.add_all([chapitre1, chapitre2])
        session.commit()

        verset1 = Verset(numero=1, texte="Andriamanitra Gen", chapitre_id=chapitre1.id)
        verset2 = Verset(numero=1, texte="Andriamanitra Exo", chapitre_id=chapitre2.id)
        session.add_all([verset1, verset2])
        session.commit()

        service = SearchService(session)
        results = service.search_versets("Andriamanitra", livre_id=livre1.id)

        assert len(results) == 1
        assert "Gen" in results[0]['texte']

    def test_search_versets_filter_by_testament(self, session):
        """Test searching verses filtered by testament."""
        livre_at = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        livre_nt = Livre(nom="Matio", abbrev="Mat", testament="NT", ordre=40)
        session.add_all([livre_at, livre_nt])
        session.commit()

        chapitre_at = Chapitre(numero=1, livre_id=livre_at.id)
        chapitre_nt = Chapitre(numero=1, livre_id=livre_nt.id)
        session.add_all([chapitre_at, chapitre_nt])
        session.commit()

        verset_at = Verset(numero=1, texte="Jesosy AT", chapitre_id=chapitre_at.id)
        verset_nt = Verset(numero=1, texte="Jesosy NT", chapitre_id=chapitre_nt.id)
        session.add_all([verset_at, verset_nt])
        session.commit()

        service = SearchService(session)
        results_at = service.search_versets("Jesosy", testament="AT")
        results_nt = service.search_versets("Jesosy", testament="NT")

        assert len(results_at) == 1
        assert "AT" in results_at[0]['texte']
        assert len(results_nt) == 1
        assert "NT" in results_nt[0]['texte']

    def test_search_results_include_reference(self, session):
        """Test that search results include book and chapter info."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset = Verset(
            numero=1,
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
            chapitre_id=chapitre.id
        )
        session.add(verset)
        session.commit()

        service = SearchService(session)
        results = service.search_versets("Andriamanitra")

        assert len(results) >= 1
        result = results[0]
        assert 'livre' in result
        assert 'chapitre' in result
        assert result['livre']['nom'] == "Genesisy"
        assert result['chapitre']['numero'] == 1
