def test_register_success(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "role": "viewer",
        },
    )

    data = response.get_json()

    assert response.status_code == 201
    assert "user_id" in data


def test_register_duplicate_email(client):
    payload = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "password123",
        "role": "viewer",
    }

    first_response = client.post("/api/auth/register", json=payload)
    second_response = client.post("/api/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "password123",
            "role": "viewer",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )

    data = response.get_json()

    assert response.status_code == 200
    assert "token" in data


def test_login_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Wrong Pass User",
            "email": "wrongpass@example.com",
            "password": "password123",
            "role": "viewer",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "wrongpass@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_login_missing_fields(client):
    response = client.post("/api/auth/login", json={})

    assert response.status_code == 400
