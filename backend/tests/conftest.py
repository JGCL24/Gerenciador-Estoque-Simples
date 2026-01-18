import os
import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

from app.main import app
from app.database import get_session

test_engine = create_engine(
    'sqlite:///./test.db',
    connect_args={"check_same_thread": False},
    echo=False
)

def get_test_session():
    with Session(test_engine) as session:
        yield session

@pytest.fixture(autouse=True)
def setup_database():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture
def client(setup_database):
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
