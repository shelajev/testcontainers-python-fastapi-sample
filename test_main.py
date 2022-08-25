from fastapi.testclient import TestClient
from testcontainers.mysql import MySqlContainer
from testcontainers.core.container import DockerContainer
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from database import Base
import pytest

from main import app, get_db

@pytest.fixture(scope="session")
def database_container() -> MySqlContainer:
  mysql = MySqlContainer()
  mysql.with_name("sad_tereshkova")
  with mysql:
    yield mysql

@pytest.fixture(scope="session")
def http_client(database_container: MySqlContainer):

    def get_db_override() -> Session:
        engine = create_engine(database_container.get_connection_url())
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_read_main(http_client: TestClient):
    created = http_client.post("/users/", json={
        "email": "oleg@atomicjar.com",
        "password": "hunter2"
    })
    assert created.status_code == 200

    users = http_client.get("/users/")
    assert users.status_code == 200
    assert users.json() == [{'email': 'oleg@atomicjar.com', 'id': 1, 'is_active': True, 'items': []}]

    single_user = http_client.get("/users/1")
    assert single_user.status_code == 200
    assert single_user.json() == {'email': 'oleg@atomicjar.com', 'id': 1, 'is_active': True, 'items': []}
