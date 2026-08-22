import pytest
from rest_framework import status


@pytest.mark.django_db
def test_obtain_jwt_token(api_client, employee_user):
    """Получение пары JWT-токенов."""

    response = api_client.post(
        "/api/token/",
        {
            "username": "employee_test",
            "password": "testpass123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_refresh_jwt_token(api_client, employee_user):
    """Обновление access-токена."""

    token_response = api_client.post(
        "/api/token/",
        {
            "username": "employee_test",
            "password": "testpass123",
        },
        format="json",
    )

    refresh = token_response.data["refresh"]

    response = api_client.post(
        "/api/token/refresh/",
        {
            "refresh": refresh,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_wrong_password(api_client, employee_user):
    """Неверный пароль."""

    response = api_client.post(
        "/api/token/",
        {
            "username": "employee_test",
            "password": "wrong_password",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
