from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base  = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as ex:
        print(ex.args)
    finally:
        db.close()

# For setting up direct connection to postgres
# def set_connection(dbname='fastapi_app', user='postgres', password='rootpass1234', host = 'localhost'):
#     while True:
#         try:
#             conn = psycopg2.connect(host='localhost', dbname='fastapi_app', user='postgres', password='rootpass1234', cursor_factory=RealDictCursor)
#             return conn
#         except psycopg2.Error as e:
#             print(f"Connection Error:\n{e}")
#             time.sleep(2)