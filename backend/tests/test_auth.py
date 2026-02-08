import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup():
    response = client.post("/api/auth/signup", json={
        "email": "test@example.com",
        "password": "testpass123",
        "software_level": "intermediate",
        "hardware_level": "beginner",
        "robotics_knowledge": False,
        "learning_goals": "Learn robotics"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_signin():
    # First signup
    client.post("/api/auth/signup", json={
        "email": "test2@example.com",
        "password": "testpass123",
        "software_level": "intermediate",
        "hardware_level": "beginner",
        "robotics_knowledge": False
    })
    
    # Then signin
    response = client.post("/api/auth/signin", json={
        "email": "test2@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()