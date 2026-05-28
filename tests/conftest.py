import os
import pytest

# Force environment variables before importing any app modules to ensure testing database isolation
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["FLASK_ENV"] = "testing"

from app import create_app
from app.database import Base, engine, db_session


@pytest.fixture(scope="session")
def app():
    """Create and configure a Flask application for testing."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture(scope="session")
def client(app):
    """A test client for the application."""
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """Create all database tables before a test, and drop them after.

    This ensures complete test case isolation.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    db_session.remove()
