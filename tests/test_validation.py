import pytest
from rest_framework import status


@pytest.mark.django_db
def test_create_ticket_without_title(api_client, employee_user):
    """Нельзя создать заявку без темы."""

    api_client.force_authenticate(user=employee_user)

    payload = {
        "description": "Описание",
        "category": "software",
        "priority": "medium",
        "status": "new",
        "author": employee_user.id,
        "assigned_to": None,
    }

    response = api_client.post(
        "/api/tickets/",
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data


@pytest.mark.django_db
def test_create_ticket_without_description(api_client, employee_user):
    """Нельзя создать заявку без описания."""

    api_client.force_authenticate(user=employee_user)

    payload = {
        "title": "Не работает Outlook",
        "category": "software",
        "priority": "medium",
        "status": "new",
        "author": employee_user.id,
        "assigned_to": None,
    }

    response = api_client.post(
        "/api/tickets/",
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "description" in response.data


@pytest.mark.django_db
def test_create_ticket_with_invalid_category(api_client, employee_user):
    """Нельзя использовать несуществующую категорию."""

    api_client.force_authenticate(user=employee_user)

    payload = {
        "title": "Ошибка",
        "description": "Описание",
        "category": "invalid_category",
        "priority": "medium",
        "status": "new",
        "author": employee_user.id,
        "assigned_to": None,
    }

    response = api_client.post(
        "/api/tickets/",
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "category" in response.data
