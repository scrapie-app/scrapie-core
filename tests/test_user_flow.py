from fastapi.testclient import TestClient
from src import main
import pytest

client = TestClient(main.scrapieApi)

@pytest.mark.skip(reason="Dont test yet")
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

def test_user_test_ping():
    user_id = 1
    response = client.get(f"/user/{user_id}")
    user = response.json()
    assert response.status_code == 200
    email = user.get("email")
    api_key = user.get("api_key")
    quota = user.get("quota")
    login_auth = client.post("/login", json={
        "email": email,
        "api_key": api_key
    })
    assert login_auth.status_code == 200
    login_auth_response = login_auth.json()
    bearer_token = login_auth_response.get("bearer_token")
    ping_test_scrape = client.get("/scrape/ping", headers={
        "Authorization": f"Bearer {bearer_token}"
    }, 
    json={
        "name": "test_ping",
        "url": "https://google.com/"
    })

    assert ping_test_scrape.status_code == 200
    response_user_next = client.get(f"/user/{user_id}")
    assert response_user_next.status_code == 200
    assert response_user_next.json().get("quota") == quota - 1