import pytest
from rest_framework import status


@pytest.mark.django_db
def test_statistics_endpoint(api_client, manager_user, tickets):
    """Получение статистики по заявкам."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/statistics/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_tickets"] == 4
    assert response.data["open_tickets"] == 3
    assert response.data["closed_tickets"] == 1
    assert response.data["critical_tickets"] == 1

    assert "by_status" in response.data
    assert "by_priority" in response.data
    assert "by_category" in response.data
