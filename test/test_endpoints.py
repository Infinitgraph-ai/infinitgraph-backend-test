"""
Tests for the FastAPI endpoints in the Infinitgraph.ai application.

"""

import pytest
from fastapi.testclient import TestClient
import json
import app.llm_client as llm_client

# Import your FastAPI app
from app.main import app

app.dependency_overrides["get_llm_function"] = lambda: llm_client.mock_generate


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """
    This fixture provides authentication headers for protected endpoints by directly
    creating a JWT token rather than going through the /api/token endpoint.
    """
    def _get_auth_headers(role):
        from app.auth import create_access_token
        username = "admin" if role == "admin" else "user"
        token = create_access_token(data={"sub": username})
        return {"Authorization": f"Bearer {token}"}
    return _get_auth_headers


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


def test_authentication(client):
    # Test Failed Authentication
    payload = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/api/token", data=payload)
    assert response.status_code == 401
    
    # Test Successful Authentication
    payload = {
        "username": "admin",
        "password": "adminpass"
    }
    response = client.post("/api/token", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_analyze_text(client, auth_headers):
    # Test without authentication
    payload = {
        "text": "This is a test text",
        "analysis_type": "invalid_analysis_type "
    }
    auth_headers= auth_headers(client)
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 401

    # Test with invalid input but proper authentication
    response = client.post("/api/analyze", json=payload, headers=auth_headers)
    assert response.status_code == 422

    # Test with valid input and authentication for "summary" analysis type
    payload = {
        "text": "This is a test text",
        "analysis_type": "summary"
    }
    response = client.post("/api/analyze", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "analysis_type" in data
    assert data["analysis_type"] == "summary"

    # Test with valid input and authentication for "sentiment" analysis type
    
    payload = {
        "text": "This a sentiment analysis test",
        "analysis_type": "sentiment"
    }
    response = client.post("/api/analyze", json=payload, headers=auth_headers)
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "analysis_type" in data
    assert data["analysis_type"] == "sentiment"

    # Test with valid input and authentication for "keywords" analysis type
    payload = {
        "text": "This is a keywords test text",
        "analysis_type": "keywords"
    }
    response = client.post("/api/analyze", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "keywords" in data
    assert "analysis_type" in data
    assert data["analysis_type"] == "keywords"

    # Test with valid input and authentication for "entities" analysis type
    payload = {
        "text": "This is a entities test text",
        "analysis_type": "entities"
    }
    response = client.post("/api/analyze", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "entities" in data
    assert "analysis_type" in data
    assert data["analysis_type"] == "entities"

    # Test with valid input and authentication for "classification" analysis type
    payload = {
        "text": "This is a classification test text",
        "analysis_type": "classification"
    }
    response = client.post("/api/analyze", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "classification" in data
    assert "analysis_type" in data
    assert data["analysis_type"] == "classification"
    





def test_get_users(client, auth_headers):
    # Test without authentication
    response = client.get("/api/users")
    assert response.status_code == 401

    # Test with authentication as user 
    user_headers = auth_headers("user")
    response = client.get("/api/users", headers=user_headers)
    assert response.status_code == 403

    # Test with authentication as admin
    admin_headers = auth_headers("admin")
    response = client.get("/api/users", headers=admin_headers)
    assert response.status_code == 200

