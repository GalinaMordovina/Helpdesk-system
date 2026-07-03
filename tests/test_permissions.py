import pytest
from rest_framework import status


@pytest.mark.django_db
def test_ticket_list_requires_authentication(api_client):
    """Без авторизации список заявок недоступен."""

    response = api_client.get("/api/tickets/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_ticket_list_for_employee(api_client, employee_user):
    """Авторизованный сотрудник может получить список заявок."""

    api_client.force_authenticate(user=employee_user)

    response = api_client.get("/api/tickets/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_ticket_list_for_support(api_client, support_user):
    """Авторизованный специалист может получить список заявок."""

    api_client.force_authenticate(user=support_user)

    response = api_client.get("/api/tickets/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_ticket_list_for_manager(api_client, manager_user):
    """Авторизованный менеджер может получить список заявок."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/tickets/")

    assert response.status_code == status.HTTP_200_OK
