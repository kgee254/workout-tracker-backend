def test_signup_success(client):
    response = client.post(
        "/signup",
        json={"username": "newuser", "password": "password123"},
    )

    assert response.status_code == 201
    assert response.get_json()["user"]["username"] == "newuser"


def test_signup_duplicate_username(client):
    response = client.post(
        "/signup",
        json={"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 409


def test_login_success(client):
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_invalid_password(client):
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "wrongpassword"},
    )

    assert response.status_code == 401


def test_me_requires_token(client):
    response = client.get("/me")

    assert response.status_code == 401


def test_me_with_token(client, auth_headers):
    response = client.get("/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.get_json()["username"] == "testuser"