from fastapi.testclient import TestClient
from src import main

client = TestClient(main.scrapieApi)

def test_create_user():
    response = client.post("/user", json={
        "email": "hello@hello.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json().get("email") == "hello@hello.com"
    assert response.json().get("id") is not None
    assert response.json().get("password") is None
    assert response.json().get("created_at") is not None
    assert response.json().get("updated_at") is not None
    assert response.json().get("quota") == 100

    