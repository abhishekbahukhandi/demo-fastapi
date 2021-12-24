import pytest
from fastapi.testclient import TestClient
from app.anc.database import get_db, Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
