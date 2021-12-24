import pytest
from app.anc import schema, config
from jose import jwt

def test_create_user(client):
    r = client.post("/users/", json={"email": "leo@abc.com", "password": "leo123"})    
    assert r.status_code == 201, r.text
    new_user = schema.UserResponse(**r.json())
    assert new_user.email == "leo@abc.com"
    
def test_get_user(client, test_user):
    r = client.get(f"/users/{test_user['id']}")
    assert r.status_code == 200, r.text
    selected_user = schema.UserResponse(**r.json())
    assert selected_user.email == "test@abc.com"

def test_login(client, test_user):
    r = client.post("/login", data = {"username": test_user["email"], "password": test_user["password"]})
    assert r.status_code == 200
    login_r = schema.Token(**r.json())
    payload = jwt.decode(login_r.access_token, config.settings.secret_key, algorithms=[config.settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_r.token_type == 'bearer'

@pytest.mark.parametrize('email, password, status_code', [
    ('test@abc.com', 'wrong password', 403,),
    ('test1@abc.com', 'test123', 403,),
    ('test1@abc.com', 'test1', 403,),
    (None, 'test123', 422,),
    ('test@abc.com', None, 422,)
    ])
def test_incorrect_login(client, email, password, status_code):
    r = client.post("/login", data = {"username": email, "password": password})
    assert r.status_code == status_code
    
