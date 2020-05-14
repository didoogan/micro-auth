import pytest

from starlette.testclient import TestClient

from main import app
from database import database
from users.models import users
import utils


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture(scope='session')
def db():
    return database


@pytest.fixture(autouse=True)
async def clear_tables(db):
    yield
    await db.execute(users.delete())


@pytest.fixture
def user_data():
    return {'email': 'test3@test.com', 'password': 'password'}


@pytest.fixture
def user_manager():
    return utils.UserManager()
