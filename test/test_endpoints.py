"""
Tests for the FastAPI endpoints in the Infinitgraph.ai application.

"""

import pytest
from fastapi.testclient import TestClient
import json

# Import your FastAPI app
from src.infinitgraph_fastapi.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """
    This fixture provides authentication headers for protected endpoints.
    
    Note: In a real implementation, this would use the actual authentication.
    For this test example, we're using a mock token.
    
    The candidate should implement proper authentication tests.
    """
    # Example token - this is just a placeholder
    # In your implementation, you should generate a real token
    mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNjE2MjM5MDIyfQ.mock-signature"
    
    return {"Authorization": f"Bearer {mock_token}"}


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_api_docs_redirect(client):
    """Test that the root endpoint redirects to docs"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"