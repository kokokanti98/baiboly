"""
Pytest configuration and shared fixtures for Baiboly backend tests.
"""
import os
import pytest
from src.app import create_app, db as _db


@pytest.fixture(scope="session")
def app():
    """
    Create application instance for testing.
    Uses testing configuration with in-memory SQLite database.
    """
    # Set testing environment
    os.environ["FLASK_ENV"] = "testing"

    # Create app with testing config
    app = create_app("testing")

    # Establish application context
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def db(app):
    """
    Create database instance and initialize schema for tests.
    Scope: session - database created once per test session.
    """
    # Create all tables
    _db.create_all()

    yield _db

    # Cleanup: drop all tables after tests
    _db.drop_all()


@pytest.fixture(scope="function")
def session(db):
    """
    Create a new database session for each test function.
    Automatically rolls back changes after each test.
    """
    connection = db.engine.connect()
    transaction = connection.begin()

    # Bind session to connection
    session = db.create_scoped_session(
        options={"bind": connection, "binds": {}}
    )
    db.session = session

    yield session

    # Rollback transaction and close connection
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope="function")
def client(app, session):
    """
    Create Flask test client for API endpoint testing.
    """
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """
    Create Flask CLI test runner for command testing.
    """
    return app.test_cli_runner()


# Sample data fixtures (to be expanded in Phase 3)

@pytest.fixture
def sample_livre_data():
    """
    Sample Bible book data for testing.
    """
    return {
        "nom": "Genesisy",
        "abbrev": "Gen",
        "testament": "AT",
        "ordre": 1,
    }


@pytest.fixture
def sample_chapitre_data():
    """
    Sample Bible chapter data for testing.
    """
    return {
        "numero": 1,
        "livre_id": 1,
    }


@pytest.fixture
def sample_verset_data():
    """
    Sample Bible verse data for testing.
    """
    return {
        "numero": 1,
        "texte": "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
        "chapitre_id": 1,
    }


@pytest.fixture
def sample_chant_data():
    """
    Sample hymn data for testing.
    """
    return {
        "numero": 1,
        "titre": "Andriamanitra no Havako",
        "paroles": "Andriamanitra no Havako...",
        "collection": "FFPM",
    }
