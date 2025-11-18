"""
TDD Tests for Bible models (Livre, Chapitre, Verset).
These tests must FAIL initially, then pass after implementation.
Constitutional requirement: TDD workflow enforced.
"""
import pytest
from src.models.bible import Livre, Chapitre, Verset
from sqlalchemy.exc import IntegrityError


@pytest.mark.unit
@pytest.mark.bible
class TestLivreModel:
    """Test suite for Livre (Bible book) model."""

    def test_livre_creation(self, session, sample_livre_data):
        """Test creating a Livre instance."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        assert livre.id is not None
        assert livre.nom == "Genesisy"
        assert livre.abbrev == "Gen"
        assert livre.testament == "AT"
        assert livre.ordre == 1

    def test_livre_nom_required(self, session):
        """Test that nom (name) is required."""
        livre = Livre(abbrev="Gen", testament="AT", ordre=1)
        session.add(livre)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_livre_abbrev_required(self, session):
        """Test that abbrev (abbreviation) is required."""
        livre = Livre(nom="Genesisy", testament="AT", ordre=1)
        session.add(livre)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_livre_testament_required(self, session):
        """Test that testament is required."""
        livre = Livre(nom="Genesisy", abbrev="Gen", ordre=1)
        session.add(livre)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_livre_ordre_required(self, session):
        """Test that ordre (order) is required."""
        livre = Livre(nom="Genesisy", abbrev="Gen", testament="AT")
        session.add(livre)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_livre_nom_unique(self, session, sample_livre_data):
        """Test that livre nom must be unique."""
        livre1 = Livre(**sample_livre_data)
        session.add(livre1)
        session.commit()

        livre2 = Livre(**sample_livre_data)
        session.add(livre2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_livre_ordre_unique(self, session, sample_livre_data):
        """Test that livre ordre must be unique per testament."""
        livre1 = Livre(**sample_livre_data)
        session.add(livre1)
        session.commit()

        livre2 = Livre(
            nom="Exode",
            abbrev="Exo",
            testament="AT",
            ordre=1  # Same ordre as Genesisy
        )
        session.add(livre2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_livre_chapitres_relationship(self, session, sample_livre_data):
        """Test that Livre has relationship with Chapitres."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        # Should have chapitres attribute
        assert hasattr(livre, 'chapitres')
        assert isinstance(livre.chapitres, list)
        assert len(livre.chapitres) == 0

    def test_livre_repr(self, session, sample_livre_data):
        """Test Livre string representation."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        repr_str = repr(livre)
        assert "Genesisy" in repr_str or "Gen" in repr_str

    def test_livre_to_dict(self, session, sample_livre_data):
        """Test Livre serialization to dictionary."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        livre_dict = livre.to_dict()
        assert isinstance(livre_dict, dict)
        assert livre_dict['nom'] == "Genesisy"
        assert livre_dict['abbrev'] == "Gen"
        assert livre_dict['testament'] == "AT"
        assert livre_dict['ordre'] == 1
        assert 'id' in livre_dict


@pytest.mark.unit
@pytest.mark.bible
class TestChapitreModel:
    """Test suite for Chapitre (Bible chapter) model."""

    def test_chapitre_creation(self, session, sample_livre_data, sample_chapitre_data):
        """Test creating a Chapitre instance."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        assert chapitre.id is not None
        assert chapitre.numero == 1
        assert chapitre.livre_id == livre.id

    def test_chapitre_numero_required(self, session, sample_livre_data):
        """Test that numero is required."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        chapitre = Chapitre(livre_id=livre.id)
        session.add(chapitre)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_chapitre_livre_id_required(self, session):
        """Test that livre_id foreign key is required."""
        chapitre = Chapitre(numero=1)
        session.add(chapitre)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_chapitre_unique_per_livre(self, session, sample_livre_data):
        """Test that chapitre numero must be unique per livre."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        chapitre1 = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre1)
        session.commit()

        chapitre2 = Chapitre(numero=1, livre_id=livre.id)
        session.add(chapitre2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_chapitre_livre_relationship(self, session, sample_livre_data, sample_chapitre_data):
        """Test that Chapitre has relationship with Livre."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        assert chapitre.livre == livre
        assert livre.chapitres[0] == chapitre

    def test_chapitre_versets_relationship(self, session, sample_livre_data, sample_chapitre_data):
        """Test that Chapitre has relationship with Versets."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        assert hasattr(chapitre, 'versets')
        assert isinstance(chapitre.versets, list)
        assert len(chapitre.versets) == 0

    def test_chapitre_repr(self, session, sample_livre_data, sample_chapitre_data):
        """Test Chapitre string representation."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        repr_str = repr(chapitre)
        assert "1" in repr_str or "Gen" in repr_str

    def test_chapitre_to_dict(self, session, sample_livre_data, sample_chapitre_data):
        """Test Chapitre serialization to dictionary."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        chapitre_dict = chapitre.to_dict()
        assert isinstance(chapitre_dict, dict)
        assert chapitre_dict['numero'] == 1
        assert chapitre_dict['livre_id'] == livre.id
        assert 'id' in chapitre_dict


@pytest.mark.unit
@pytest.mark.bible
class TestVersetModel:
    """Test suite for Verset (Bible verse) model."""

    def test_verset_creation(self, session, sample_livre_data, sample_chapitre_data, sample_verset_data):
        """Test creating a Verset instance."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        sample_verset_data['chapitre_id'] = chapitre.id
        verset = Verset(**sample_verset_data)
        session.add(verset)
        session.commit()

        assert verset.id is not None
        assert verset.numero == 1
        assert verset.texte == "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany."
        assert verset.chapitre_id == chapitre.id

    def test_verset_numero_required(self, session, sample_livre_data, sample_chapitre_data):
        """Test that numero is required."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        verset = Verset(
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
            chapitre_id=chapitre.id
        )
        session.add(verset)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_verset_texte_required(self, session, sample_livre_data, sample_chapitre_data):
        """Test that texte (text) is required."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        verset = Verset(numero=1, chapitre_id=chapitre.id)
        session.add(verset)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_verset_chapitre_id_required(self, session):
        """Test that chapitre_id foreign key is required."""
        verset = Verset(
            numero=1,
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany."
        )
        session.add(verset)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_verset_unique_per_chapitre(self, session, sample_livre_data, sample_chapitre_data):
        """Test that verset numero must be unique per chapitre."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        verset1 = Verset(
            numero=1,
            texte="Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
            chapitre_id=chapitre.id
        )
        session.add(verset1)
        session.commit()

        verset2 = Verset(
            numero=1,
            texte="Another text",
            chapitre_id=chapitre.id
        )
        session.add(verset2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_verset_chapitre_relationship(self, session, sample_livre_data, sample_chapitre_data, sample_verset_data):
        """Test that Verset has relationship with Chapitre."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        sample_verset_data['chapitre_id'] = chapitre.id
        verset = Verset(**sample_verset_data)
        session.add(verset)
        session.commit()

        assert verset.chapitre == chapitre
        assert chapitre.versets[0] == verset

    def test_verset_texte_search_vector(self, session, sample_livre_data, sample_chapitre_data, sample_verset_data):
        """Test that Verset has texte_search_vector for full-text search."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        sample_verset_data['chapitre_id'] = chapitre.id
        verset = Verset(**sample_verset_data)
        session.add(verset)
        session.commit()

        # Check that texte_search_vector column exists
        assert hasattr(verset, 'texte_search_vector')

    def test_verset_repr(self, session, sample_livre_data, sample_chapitre_data, sample_verset_data):
        """Test Verset string representation."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        sample_verset_data['chapitre_id'] = chapitre.id
        verset = Verset(**sample_verset_data)
        session.add(verset)
        session.commit()

        repr_str = repr(verset)
        assert "1" in repr_str

    def test_verset_to_dict(self, session, sample_livre_data, sample_chapitre_data, sample_verset_data):
        """Test Verset serialization to dictionary."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        sample_verset_data['chapitre_id'] = chapitre.id
        verset = Verset(**sample_verset_data)
        session.add(verset)
        session.commit()

        verset_dict = verset.to_dict()
        assert isinstance(verset_dict, dict)
        assert verset_dict['numero'] == 1
        assert verset_dict['texte'] == "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany."
        assert verset_dict['chapitre_id'] == chapitre.id
        assert 'id' in verset_dict

    def test_verset_to_dict_with_references(self, session, sample_livre_data, sample_chapitre_data, sample_verset_data):
        """Test Verset serialization with livre and chapitre references."""
        livre = Livre(**sample_livre_data)
        session.add(livre)
        session.commit()

        sample_chapitre_data['livre_id'] = livre.id
        chapitre = Chapitre(**sample_chapitre_data)
        session.add(chapitre)
        session.commit()

        sample_verset_data['chapitre_id'] = chapitre.id
        verset = Verset(**sample_verset_data)
        session.add(verset)
        session.commit()

        verset_dict = verset.to_dict(include_references=True)
        assert 'livre' in verset_dict
        assert 'chapitre' in verset_dict
        assert verset_dict['livre']['nom'] == "Genesisy"
        assert verset_dict['chapitre']['numero'] == 1
