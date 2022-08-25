# A sample FastApi application with Testcontainers-python tests

This is a very basic [FastApi](https://fastapi.tiangolo.com/) application from the [user guide about accessing SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) from a FastApi app.

## Setup 

Requires Python 3.10, other versions might work. 

Install the dependencies:
```
python -m pip install --upgrade pip
pip install flake8 pytest
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

Run the application: 
```
uvicorn main:app --reload
```

In the local development mode our application uses SQLite database. 
You can access the Swagger UI at the [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), and use it to perform API calls:

![Swagger UI for the sample app](https://user-images.githubusercontent.com/426039/186758562-377a6e29-5822-41ca-8bdf-c1c82ba19d4c.png)

## Running tests 

Tests are implemented using Testcontainers-python for managing an ephemeral instance of MySQL database in a Docker container. 

MySQL container is created and being run by a pytest fixture: 

```
@pytest.fixture(scope="session")
def database_container() -> MySqlContainer:
  mysql = MySqlContainer()
  with mysql:
    yield mysql
``` 

And another fixture that creates the app for the test, and a HTTP client for accessing the app, overrides the default function for getting the database connection, which normally uses SQLite as we saw above. 

```
@pytest.fixture(scope="session")
def http_client(database_container: MySqlContainer):
``` 

It uses `MySqlContainer` and configures the sqlalchemy engine with the database url from the container:
```
database_container.get_connection_url()
```

You can run the tests with:

```
pytest
``` 
