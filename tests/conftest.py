import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provides a TestClient for testing the FastAPI application"""
    return TestClient(app)
