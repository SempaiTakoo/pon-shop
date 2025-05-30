import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.user_service.old_app.database.base import Base


DB_URL = ''
engine = create_engine(DB_URL)
TestingSession = sessionmaker(bind=engine)


@pytest.fixture(scope='session', autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='session')
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSession(bind=connection)

    yield session

    session.close()
    transaction.close()
    connection.close()
