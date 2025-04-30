"""
Tests for the FastAPI endpoints in the Infinitgraph.ai application.

"""

import pytest
from fastapi.testclient import TestClient
import datetime
import jwt

# Import your FastAPI app
from app.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """
    This fixture provides authentication headers for protected endpoints.
    
    Dynamically generates a valid JWT token for the specified user role.
    """
    def generate_headers(username):
        secret_key = "my-secret-key"
        payload = {
            "sub": username,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=30),
            "iat": datetime.datetime.now(),
            "nbf": datetime.datetime.now()
        }
        token = jwt.encode(payload, key=secret_key, algorithm="HS256")
        return {"Authorization": f"Bearer {token}"}

    return generate_headers


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


def test_api_token(client):
    """Test the /api/token endpoint for authentication"""
    # Valid credentials
    response = client.post("/api/token", data={"username": "admin", "password": "adminpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Invalid credentials
    response = client.post("/api/token", data={"username": "admin", "password": "wrongpass"})
    assert response.status_code == 401
    data = response.json()
    assert data["status"] == 401
    assert "Invalid credentials" in data["message"]

def test_api_analyze(client, auth_headers):
    """Test the /api/analyze endpoint for text analysis"""
    # Valid analysis request
    response = client.post(
        "/api/analyze",
        json={"text": "This is a test text for analysis.", "analysis_type": "summary"},
        headers=auth_headers("user")
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analysis_type"] == "summary"
    assert "summary" in data

    # Invalid analysis type
    response = client.post(
        "/api/analyze",
        json={"text": "This is a test text for analysis.", "analysis_type": "invalid_type"},
        headers=auth_headers("user")
    )
    assert response.status_code == 422

def test_api_users_admin_access(client, auth_headers):
    """Test the /api/users endpoint for admin access"""
    # admin token
    admin_headers = auth_headers("admin")
    response = client.get("/api/users", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) > 0

    # non admin token
    user_headers = auth_headers("user")
    response = client.get("/api/users", headers=user_headers)
    assert response.status_code == 403
    data = response.json()
    assert data["status"] == 403
    assert "Access denied" in data["message"]

def test_api_history_user_access(client, auth_headers):
    """Test the /api/history endpoint for user-specific access"""
    # user token
    user_headers = auth_headers("user")
    response = client.get("/api/history", headers=user_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert all(item["user_id"] == 2 for item in data["items"])  # ID 2 is "user"

    # admin token (should see their own history only)
    admin_headers = auth_headers("admin")
    response = client.get("/api/history", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert all(item["user_id"] == 1 for item in data["items"])  # ID 1 is "admin"