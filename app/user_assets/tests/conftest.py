import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from starlette.testclient import TestClient

from initial_data import initial_base_user
from main import app
from system.config import settings
from system.dbs.models import Base
from system.dbs.postgre import get_db
from user.models.user import UsrUser

DB_TEST_URL = f"{str(settings.POSTGRES_DATABASE_URL)}_test"
engine = create_engine(settings.POSTGRES_DATABASE_URL + "_test", echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(DB_TEST_URL)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='function')
def initiate_user_and_permissions(db):
    initial_base_user(session=db)
    user = db.query(UsrUser).all()[0]
    return user
