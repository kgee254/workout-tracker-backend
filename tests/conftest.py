import pytest

from app import create_app
from extensions import db, bcrypt
from models import User


@pytest.fixture
def app(tmp_path):
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}",
        "JWT_SECRET_KEY": "test-secret-key",
    })

    with app.app_context():
        # Remove any existing database tables and create fresh test tables.
        db.drop_all()
        db.create_all()

        user = User(
            username="testuser",
            password_hash=bcrypt.generate_password_hash(
                "password123"
            ).decode("utf-8"),
        )

        db.session.add(user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def token(client):
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "password123"},
    )
    return response.get_json()["access_token"]


@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}