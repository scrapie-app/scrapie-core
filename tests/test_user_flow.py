from fastapi.testclient import TestClient
from src import main
from faker import Faker

client = TestClient(main.scrapieApi)
fake = Faker()

def create_user():
    fake_email = fake.email()
    fake_password = fake.password()
    response = client.post("/user", json={
        "email": fake_email,
        "password": fake_password
    })
    return [response, fake_email, fake_password]

def test_create_user():
    [response, _, _] = create_user()
    assert response.status_code == 200
    assert response.json().get("id") is not None
    assert response.json().get("password") is None
    assert response.json().get("created_at") is not None
    assert response.json().get("updated_at") is not None
    assert response.json().get("quota") == 100

def test_user_test_ping():
    [user_data, email, password] = create_user()
    user_id = user_data.json().get("id")
    response = client.get(f"/user/{user_id}")
    user = response.json()
    assert response.status_code == 200
    email = user.get("email")
    api_key = user.get("api_key")
    quota = user.get("quota")
    login_auth = client.post("/login", json={
        "email": email,
        "password": password
    })
    assert login_auth.status_code == 200
    login_auth_response = login_auth.json()
    bearer_token = login_auth_response.get("bearer_token")
    ping_test_scrape = client.get("/scrape/ping", 
        headers={
            "Authorization": f"Bearer {bearer_token}"
        }, 
        json={
            "name": "test_ping",
            "url": "https://google.com/"
        }
    )
    assert ping_test_scrape.status_code == 200
    response_user_next = client.get(f"/user/{user_id}")
    assert response_user_next.status_code == 200
    assert response_user_next.json().get("quota") == quota - 1
