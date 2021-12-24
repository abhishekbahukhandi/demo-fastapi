from _pytest import python
import pytest
from fastapi.testclient import TestClient
from app.anc.database import get_db, Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.anc.oauth2 import create_access_token
from app.anc import models
#from alembic import command

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rootpass1234@localhost:5432/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)

#client = TestClient(app)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    except Exception as ex:
        print(ex.args)
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    #command.upgrade("head")
    def override_get_db():
        try:
            yield session
        except Exception as ex:
            print(ex.args)
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    #command.downgrade("base")

@pytest.fixture
def test_user(client):
    test_user = {'email': 'test@abc.com', 'password': 'test123'}
    r = client.post("/users/", json = test_user)
    assert r.status_code == 201
    new_user = {**r.json(), "password": test_user["password"]}
    return new_user

@pytest.fixture
def test_user2(client):
    test_user = {'email': 'test12@abc.com', 'password': 'test1234'}
    r = client.post("/users/", json = test_user)
    assert r.status_code == 201
    new_user = {**r.json(), "password": test_user["password"]}
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [
        {'title': 'First Post', 'content': 'This is first post', 'published': False, 'owner_id': test_user["id"]}, 
        {'title': 'Second Post', 'content': 'This is second post', 'published': False, 'owner_id': test_user["id"]}, 
        {'title': 'Third Post', 'content': 'This is third post', 'published': True, 'owner_id': test_user["id"]},
        {'title': 'Fourth Post', 'content': 'This is fourth post', 'published': False, 'owner_id': test_user2["id"]}
    ]    
    #mapped_posts = map(lambda x: models.Post(**x), post_data)
    #posts = list(mapped_posts)
    posts = [models.Post(**x) for x in post_data]
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all() 