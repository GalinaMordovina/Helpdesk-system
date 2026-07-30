import pytest
from django.urls import reverse

from tickets.models import Ticket


@pytest.mark.django_db
def test_statistics_page_requires_authentication(client):
    """
    Неавторизованный пользователь перенаправляется
    на страницу входа.
    """

    response = client.get(reverse("statistics_web"))

    assert response.status_code == 302
    assert "/accounts/login/" in response.url


@pytest.mark.django_db
def test_employee_cannot_open_statistics(
    client,
    employee_user,
):
    """
    Обычный пользователь не имеет доступа
    к странице статистики.
    """

    client.force_login(employee_user)

    response = client.get(reverse("statistics_web"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_support_can_open_statistics(
    client,
    support_user,
):
    """
    Специалист поддержки имеет доступ
    к странице статистики.
    """

    client.force_login(support_user)

    response = client.get(reverse("statistics_web"))

    assert response.status_code == 200
    assert "statistics_app/statistics.html" in [
        template.name
        for template in response.templates
        if template.name
    ]


@pytest.mark.django_db
def test_manager_can_open_statistics(
    client,
    manager_user,
):
    """
    Руководитель имеет доступ
    к странице статистики.
    """

    client.force_login(manager_user)

    response = client.get(reverse("statistics_web"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_statistics_page_contains_ticket_counts(
    client,
    manager_user,
    ticket,
):
    """
    Страница передаёт в шаблон основные показатели
    статистики по заявкам.
    """

    client.force_login(manager_user)

    response = client.get(reverse("statistics_web"))

    assert response.status_code == 200
    assert response.context["total_tickets"] == Ticket.objects.count()
    assert "open_tickets" in response.context
    assert "closed_tickets" in response.context
    assert "critical_tickets" in response.context
    assert "by_status" in response.context
    assert "by_priority" in response.context
    assert "by_category" in response.context
