"""
TDD Tests for Bible API endpoints.
These tests must FAIL initially, then pass after implementation.
Constitutional requirement: TDD workflow enforced.
"""
import pytest
import json
from src.models.bible import Livre, Chapitre, Verset


@pytest.mark.integration
@pytest.mark.bible
class TestBibleAPI:
    """Test suite for Bible API endpoints."""

    def test_get_livres_endpoint(self, client, session):
        """Test GET /api/bible/livres - Get all books."""
        # Create test data
        livre1 = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        livre2 = Livre(nom="Eksodosy", abbrev="Exo", testament="AT", ordre=2)
        session.add_all([livre1, livre2])
        session.commit()

        response = client.get('/api/bible/livres')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['nom'] == "Genesisy"
        assert data[1]['nom'] == "Eksodosy"

    def test_get_livres_filter_by_testament(self, client, session):
        """Test GET /api/bible/livres?testament=AT - Filter by testament."""
        livre_at = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        livre_nt = Livre(nom="Matio", abbrev="Mat", testament="NT", ordre=40)
        session.add_all([livre_at, livre_nt])
        session.commit()

        response = client.get('/api/bible/livres?testament=AT')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['testament'] == "AT"

    def test_get_livre_by_id_endpoint(self, client, session):
        """Test GET /api/bible/livres/<id> - Get book by ID."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        response = client.get(f'/api/bible/livres/{livre.id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['nom'] == "Genesisy"
        assert data['abbrev'] == "Gen"

    def test_get_livre_by_id_not_found(self, client, session):
        """Test GET /api/bible/livres/999 - Book not found."""
        response = client.get('/api/bible/livres/999')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        # Error message should be in Malagasy
        assert 'Tsy hita' in data['error'] or 'tsy hita' in data['error'].lower()

    def test_get_chapitres_by_livre_endpoint(self, client, session):
        """Test GET /api/bible/livres/<id>/chapitres - Get chapters for book."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre1 = Chapitre(numero=1, livre_id=livre.id)
        chapitre2 = Chapitre(numero=2, livre_id=livre.id)
        session.add_all([chapitre1, chapitre2])
        session.commit()

        response = client.get(f'/api/bible/livres/{livre.id}/chapitres')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['numero'] == 1
        assert data[1]['numero'] == 2

    def test_get_chapitre_by_id_endpoint(self, client, session):
        """Test GET /api/bible/chapitres/<id> - Get chapter by ID."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        response = client.get(f'/api/bible/chapitres/{chapitre.id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['numero'] == 1
        assert data['livre_id'] == livre.id

    def test_get_versets_by_chapitre_endpoint(self, client, session):
        """Test GET /api/bible/chapitres/<id>/versets - Get verses for chapter."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        verset1 = Verset(numero=1, texte="Verset 1", chapitre_id=chapitre.id)
        verset2 = Verset(numero=2, texte="Verset 2", chapitre_id=chapitre.id)
        session.add_all([verset1, verset2])
        session.commit()

        response = client.get(f'/api/bible/chapitres/{chapitre.id}/versets')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['numero'] == 1
        assert data[1]['numero'] == 2

    def test_get_verset_by_id_endpoint(self, client, session):
        """Test GET /api/bible/versets/<id> - Get verse by ID."""
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

        response = client.get(f'/api/bible/versets/{verset.id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['numero'] == 1
        assert "Andriamanitra" in data['texte']

    def test_get_verset_by_reference_endpoint(self, client, session):
        """Test GET /api/bible/reference?livre=Gen&chapitre=1&verset=1 - Get by reference."""
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

        response = client.get('/api/bible/reference?livre=Gen&chapitre=1&verset=1')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['numero'] == 1
        assert "Andriamanitra" in data['texte']

    def test_get_verset_by_reference_missing_params(self, client, session):
        """Test GET /api/bible/reference without required params - Bad request."""
        response = client.get('/api/bible/reference?livre=Gen')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_search_versets_endpoint(self, client, session):
        """Test GET /api/bible/search?q=Andriamanitra - Search verses."""
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

        response = client.get('/api/bible/search?q=Andriamanitra')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'results' in data
        assert len(data['results']) >= 1
        assert "Andriamanitra" in data['results'][0]['texte']

    def test_search_versets_with_pagination(self, client, session):
        """Test GET /api/bible/search?q=test&limit=5&offset=0 - Paginated search."""
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
                texte=f"Test verset {i}",
                chapitre_id=chapitre.id
            )
            session.add(verset)
        session.commit()

        response = client.get('/api/bible/search?q=Test&limit=5&offset=0')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['results']) == 5
        assert 'total' in data
        assert data['total'] >= 10

    def test_search_versets_empty_query(self, client, session):
        """Test GET /api/bible/search?q= - Empty query returns 400."""
        response = client.get('/api/bible/search?q=')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_search_versets_filter_by_livre(self, client, session):
        """Test GET /api/bible/search?q=test&livre_id=1 - Filter by book."""
        livre1 = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        livre2 = Livre(nom="Eksodosy", abbrev="Exo", testament="AT", ordre=2)
        session.add_all([livre1, livre2])
        session.commit()

        chapitre1 = Chapitre(numero=1, livre_id=livre1.id)
        chapitre2 = Chapitre(numero=1, livre_id=livre2.id)
        session.add_all([chapitre1, chapitre2])
        session.commit()

        verset1 = Verset(numero=1, texte="Test Gen", chapitre_id=chapitre1.id)
        verset2 = Verset(numero=1, texte="Test Exo", chapitre_id=chapitre2.id)
        session.add_all([verset1, verset2])
        session.commit()

        response = client.get(f'/api/bible/search?q=Test&livre_id={livre1.id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['results']) == 1
        assert "Gen" in data['results'][0]['texte']

    def test_search_versets_filter_by_testament(self, client, session):
        """Test GET /api/bible/search?q=test&testament=AT - Filter by testament."""
        livre_at = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        livre_nt = Livre(nom="Matio", abbrev="Mat", testament="NT", ordre=40)
        session.add_all([livre_at, livre_nt])
        session.commit()

        chapitre_at = Chapitre(numero=1, livre_id=livre_at.id)
        chapitre_nt = Chapitre(numero=1, livre_id=livre_nt.id)
        session.add_all([chapitre_at, chapitre_nt])
        session.commit()

        verset_at = Verset(numero=1, texte="Test AT", chapitre_id=chapitre_at.id)
        verset_nt = Verset(numero=1, texte="Test NT", chapitre_id=chapitre_nt.id)
        session.add_all([verset_at, verset_nt])
        session.commit()

        response = client.get('/api/bible/search?q=Test&testament=AT')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['results']) == 1
        assert "AT" in data['results'][0]['texte']

    def test_api_returns_json_content_type(self, client, session):
        """Test that API returns proper JSON content type."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        response = client.get('/api/bible/livres')

        assert response.status_code == 200
        assert response.content_type == 'application/json'

    def test_api_cors_headers(self, client, session):
        """Test that API includes CORS headers."""
        response = client.get('/api/bible/livres')

        # CORS headers should be present
        assert 'Access-Control-Allow-Origin' in response.headers

    def test_api_error_messages_in_malagasy(self, client, session):
        """Test that error messages are in Malagasy."""
        response = client.get('/api/bible/livres/999')

        assert response.status_code == 404
        data = json.loads(response.data)
        # Check that error message contains Malagasy text
        error_text = data.get('error', '')
        # Should contain Malagasy words like "Tsy hita" (not found)
        assert any(word in error_text.lower() for word in ['tsy', 'hita', 'olana'])

    def test_health_check_endpoint(self, client):
        """Test GET /api/health - Health check endpoint."""
        response = client.get('/api/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'message' in data


@pytest.mark.integration
@pytest.mark.bible
@pytest.mark.slow
class TestBibleAPIPerformance:
    """Performance tests for Bible API endpoints."""

    def test_get_livres_response_time(self, client, session):
        """Test that GET /api/bible/livres responds within 200ms."""
        import time

        # Create 66 books (realistic data)
        for i in range(1, 67):
            livre = Livre(
                nom=f"Livre {i}",
                abbrev=f"L{i}",
                testament="AT" if i <= 39 else "NT",
                ordre=i
            )
            session.add(livre)
        session.commit()

        start_time = time.time()
        response = client.get('/api/bible/livres')
        end_time = time.time()

        assert response.status_code == 200
        response_time = (end_time - start_time) * 1000  # Convert to ms
        # Constitutional requirement: API <200ms p95
        assert response_time < 200, f"Response time {response_time}ms exceeds 200ms"

    def test_search_response_time(self, client, session):
        """Test that search responds within 2000ms (constitutional requirement)."""
        import time

        # Create realistic test data
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre)
        session.commit()

        # Create 100 verses
        for i in range(1, 101):
            verset = Verset(
                numero=i,
                texte=f"Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany verset {i}",
                chapitre_id=chapitre.id
            )
            session.add(verset)
        session.commit()

        start_time = time.time()
        response = client.get('/api/bible/search?q=Andriamanitra')
        end_time = time.time()

        assert response.status_code == 200
        response_time = (end_time - start_time) * 1000  # Convert to ms
        # Constitutional requirement: Search <2s
        assert response_time < 2000, f"Search time {response_time}ms exceeds 2000ms"
