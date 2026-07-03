import pytest
from rest_framework import status


@pytest.mark.django_db
def test_filter_by_status(api_client, manager_user, tickets):
    """Фильтрация по одному статусу."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/tickets/?status=new")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["status"] == "new"


@pytest.mark.django_db
def test_filter_by_multiple_statuses(api_client, manager_user, tickets):
    """Фильтрация по нескольким статусам."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get(
        "/api/tickets/?status=new,in_progress"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_filter_by_priority(api_client, manager_user, tickets):
    """Фильтрация по приоритету."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/tickets/?priority=critical")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["priority"] == "critical"


@pytest.mark.django_db
def test_filter_by_category(api_client, manager_user, tickets):
    """Фильтрация по категории."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/tickets/?category=network")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["category"] == "network"


@pytest.mark.django_db
def test_search_by_title(api_client, manager_user, tickets):
    """Поиск по теме заявки."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/tickets/?search=Outlook")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert "Outlook" in response.data[0]["title"]


@pytest.mark.django_db
def test_ordering_by_created_at(api_client, manager_user, tickets):
    """Сортировка по дате создания."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/tickets/?ordering=created_at")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4
