
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
from alembic import command



#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:v2mayu2021@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False ,autoflush=False,bind=engine)


@pytest.fixture()
def session():
    """Provides a database session for testing purposes.

    - Drops all existing tables in the test database.
    - Creates all tables defined by the `Base` class.
    - Opens a new session.
    - Yields the session for testing.
    - Closes the session after the test completes.
    """
    # print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    """Provides a FastAPI test client with a mocked dependency for database access.

    - Creates a TestClient instance for the FastAPI application.
    - Defines a function `override_get_db` to provide the session fixture as the database connection.
    - Overrides the `get_db` dependency in the application with `override_get_db`.
    - Yields the TestClient instance.
    """

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    """Creates a test user using a POST request to the `/users/` endpoint.

    - Defines user data with email and password.
    - Sends a POST request to create a new user.
    - Asserts a successful response (status code 201).
    - Extracts the created user's information and sets the password.
    - Yields the test user data.
    """
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(test_user):
    """Generates a JWT access token for the provided test user.

    - Uses the `create_access_token` function to create a token.
    - Takes the test user's ID as the payload for the token.
    - Yields the generated access token.
    """
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client,token):
    """Provides a TestClient instance with authorization headers for authenticated requests.

    - Takes the TestClient instance and a token as arguments.
    - Sets the `Authorization` header in the client with the format `Bearer {token}`.
    - Yields the authorized TestClient instance.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data = [{
        "title":"first title",
        "content":"first content",
        "owner_id": test_user['id']
    },{
        "title":"second title",
        "content":"2nd content",
        "owner_id": test_user['id']
    },{
        "title":"3rd title",
        "content":"3rd content",
        "owner_id": test_user['id']
    },{
        "title":"4th title",
        "content":"3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model,posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title",content="first content",owner_id= test_user['id']),
    #                 models.Post(title="second title",content="2nd content",owner_id= test_user['id']),
    #                 models.Post(title="3rd title",content="3rd content",owner_id= test_user['id'])])
    session.commit()

    posts=session.query(models.Post).all()
    return posts