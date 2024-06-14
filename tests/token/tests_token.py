import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_token_create_success(api_client, user):
    payload = {"username": user.username, "password": "237"}
    response = api_client.post("/api/token/", payload, format="json")
    response_json = response.json()

    assert "refresh" in response_json
    assert "access" in response_json
    assert response.status_code == 200


@pytest.mark.parametrize(
    "payload,expected_response,status_code",
    [
        (
            {"username": "Woody Pride"},
            {"password": ["This field is required."]},
            400,
        ),
        (
            {"password": 237},
            {"username": ["This field is required."]},
            400,
        ),
        (
            {"username": "Woody Pride", "password": 237},
            {"detail": "No active account found with the given credentials"},
            401,
        ),
    ],
)
def test_token_create_error(api_client, payload, expected_response, status_code):
    response = api_client.post("/api/token/", payload, format="json")

    assert response.json() == expected_response
    assert response.status_code == status_code


def test_token_refresh_success(api_client, user):
    payload = {"username": user.username, "password": "237"}
    response = api_client.post("/api/token/", payload, format="json")
    response_json = response.json()

    refresh_payload = {"refresh": response_json["refresh"]}
    refresh_response = api_client.post(
        "/api/token/refresh/",
        refresh_payload,
        format="json",
    )
    refresh_response_json = refresh_response.json()

    assert "access" in refresh_response_json
    assert refresh_response.status_code == 200


def test_token_refresh_error(api_client):
    response = api_client.post("/api/token/refresh/", {}, format="json")

    assert response.json() == {"refresh": ["This field is required."]}
    assert response.status_code == 400


def test_token_refresh_invalid_error(api_client):
    response = api_client.post(
        "/api/token/refresh/",
        {"refresh": "1233"},
        format="json",
    )

    assert response.json() == {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid",
    }
    assert response.status_code == 401


def test_token_verify_success(api_client, user):
    payload = {"username": user.username, "password": "237"}
    response = api_client.post("/api/token/", payload, format="json")
    response_json = response.json()

    verify_payload = {"token": response_json["access"]}
    verify_response = api_client.post(
        "/api/token/verify/",
        verify_payload,
        format="json",
    )
    verify_response_json = verify_response.json()

    assert isinstance(verify_response_json, dict)
    assert verify_response.status_code == 200


def test_token_verify_error(api_client):
    response = api_client.post("/api/token/verify/", {}, format="json")

    assert response.json() == {"token": ["This field is required."]}
    assert response.status_code == 400


def test_token_verify_invalid_error(api_client):
    response = api_client.post("/api/token/verify/", {"token": "1233"}, format="json")

    assert response.json() == {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid",
    }
    assert response.status_code == 401
