"""
Configuração dos testes com pytest.

Este arquivo define fixtures compartilhadas entre todos os testes:
- setup_database: Cria e limpa o banco de dados antes/depois dos testes
- client: Fornece um cliente HTTP (TestClient) para testar a API
"""

import os
import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

# Configure variável de ambiente ANTES de importar a app
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

from app.main import app
from app.database import get_session

# Engine para banco de testes em memória (mais rápido)
test_engine = create_engine(
    'sqlite:///./test.db',
    connect_args={"check_same_thread": False},
    echo=False
)

def get_test_session():
    """Função para fornecer sessão de teste ao banco de dados."""
    with Session(test_engine) as session:
        yield session

@pytest.fixture(autouse=True)
def setup_database():
    """
    Fixture que:
    1. Cria todas as tabelas antes de cada teste
    2. Executa o teste
    3. Remove todas as tabelas após o teste (limpeza)
    
    autouse=True: Executa automaticamente para cada teste
    """
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture
def client(setup_database):
    """
    Fixture que fornece um cliente TestClient para fazer requisições HTTP.
    
    Sobrescreve a dependência get_session da aplicação para usar 
    a sessão de teste em vez do banco de produção.
    """
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
