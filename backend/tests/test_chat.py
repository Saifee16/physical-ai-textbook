import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat():
    response = client.post("/api/chat", json={
        "message": "What is ROS 2?",
        "chapter_context": "week3-5/ros2-architecture"
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data