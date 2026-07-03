import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_ticket_list(api_client, manager_user):
    """Получение списка заявок."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/tickets/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_ticket(api_client, employee_user):
    """Создание новой заявки."""

    api_client.force_authenticate(user=employee_user)

    payload = {
        "title": "Не работает Outlook",
        "description": "Ошибка при запуске приложения.",
        "category": "software",
        "priority": "high",
        "status": "new",
        "author": employee_user.id,
        "assigned_to": None,
    }

    response = api_client.post(
        "/api/tickets/",
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == payload["title"]
    assert response.data["status"] == "new"
