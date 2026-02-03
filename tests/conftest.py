import pytest
import os
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool

from src.main import app
from src.config.database import get_session
from src.models import Base


@pytest.fixture(scope="session")
def test_db():
    """Fixture pour une base de données de test"""
    # Utilise une base de données SQLite en mémoire pour les tests
    engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False
    )
    
    Base.metadata.create_all(engine)
    
    Session.configure(bind=engine)
    yield Session()
    
    Session.remove_all()


@pytest.fixture
def client(test_db):
    """Fixture client FastAPI avec base de données de test"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def session(test_db):
    """Fixture session pour les tests"""
    yield test_db
