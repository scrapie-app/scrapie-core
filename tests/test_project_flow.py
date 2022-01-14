from fastapi.testclient import TestClient
from src import main
from faker import Faker

client = TestClient(main.scrapieApi)
Faker.seed(0)
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

def test_project_flow():
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
    project_name = fake.bothify(text='Project ????-########', letters='ABCDE')
    project_description = fake.bothify(text='Project Description ????-########', letters='ABCDE')
    api_keys_for_user = client.get('/api/keys',
        headers={
            "Authorization": f"Bearer {bearer_token}"
        },
    )
    assert api_keys_for_user.status_code == 200
    api_key_id = api_keys_for_user.json().get("api_keys")[0].get("id")
    print(api_key_id, project_name, project_description)
    create_project = client.post("/project/create", 
        headers={
            "Authorization": f"Bearer {bearer_token}"
        }, 
        json={
            "name": project_name,
            "description": project_description,
            "api_key_id": api_key_id
        }
    )
    assert create_project.status_code == 200
    project_id = create_project.json().get("id")
    assert create_project.json().get("id") > 0
    all_projects = client.get('/project/all',
        headers={
            "Authorization": f"Bearer {bearer_token}"
        },
    )
    assert all_projects.status_code == 200
    assert len(all_projects.json().get("projects")) == 1
    delete_project = client.post("/project/delete", 
        headers={
            "Authorization": f"Bearer {bearer_token}"
        }, 
        json={
            "id": project_id
        }
    )
    assert delete_project.status_code == 200
