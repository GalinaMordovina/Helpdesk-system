import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from tickets.models import Ticket


User = get_user_model()


@pytest.fixture
def user(db):
    """
    Создаёт пользователя для проверки веб-интерфейса.
    """
    return User.objects.create_user(
        username="testuser",
        password="testpassword123",
    )


@pytest.fixture
def authenticated_client(client, user):
    """
    Авторизует тестового пользователя.
    """
    client.force_login(user)
    return client


@pytest.fixture
def ticket(user):
    """
    Создаёт тестовую заявку.
    """
    return Ticket.objects.create(
        title="Не работает принтер",
        description="Принтер не печатает документы",
        category=Ticket.Category.PRINTER,
        priority=Ticket.Priority.MEDIUM,
        status=Ticket.Status.NEW,
        author=user,
    )


@pytest.mark.django_db
def test_ticket_list_requires_authentication(client):
    """
    Неавторизованный пользователь перенаправляется
    на страницу входа.
    """
    response = client.get(reverse("ticket_list"))

    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_ticket_list_available_for_authenticated_user(
    authenticated_client,
):
    """
    Авторизованный пользователь может открыть список заявок.
    """
    response = authenticated_client.get(reverse("ticket_list"))

    assert response.status_code == 200
    assert "tickets/ticket_list.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_ticket_list_displays_ticket(
    authenticated_client,
    ticket,
):
    """
    Созданная заявка отображается в общем списке.
    """
    response = authenticated_client.get(reverse("ticket_list"))

    assert response.status_code == 200
    assert ticket.title in response.content.decode()


@pytest.mark.django_db
def test_ticket_detail_available(
    authenticated_client,
    ticket,
):
    """
    Авторизованный пользователь может открыть карточку заявки.
    """
    response = authenticated_client.get(
        reverse("ticket_detail", kwargs={"pk": ticket.pk})
    )

    assert response.status_code == 200
    assert ticket.title in response.content.decode()
    assert ticket.description in response.content.decode()


@pytest.mark.django_db
def test_ticket_create(
    authenticated_client,
    user,
):
    """
    Авторизованный пользователь может создать заявку.
    """
    data = {
        "title": "Не работает компьютер",
        "description": "Компьютер не включается",
        "category": Ticket.Category.PRINTER,
        "priority": Ticket.Priority.HIGH,
        "status": Ticket.Status.NEW,
    }

    response = authenticated_client.post(
        reverse("ticket_create"),
        data=data,
    )

    assert response.status_code == 302
    assert Ticket.objects.filter(
        title="Не работает компьютер",
        author=user,
    ).exists()


@pytest.mark.django_db
def test_ticket_update(
    authenticated_client,
    ticket,
):
    """
    Авторизованный сотрудник может изменить данные заявки,
    сохранив её текущий статус.
    """
    data = {
        "title": "Принтер работает с ошибками",
        "description": "Принтер печатает документы с полосами",
        "category": ticket.category,
        "priority": Ticket.Priority.HIGH,
        "status": ticket.status,
    }

    response = authenticated_client.post(
        reverse(
            "ticket_update",
            kwargs={"pk": ticket.pk},
        ),
        data=data,
    )

    ticket.refresh_from_db()

    assert response.status_code == 302
    assert ticket.title == "Принтер работает с ошибками"
    assert ticket.description == "Принтер печатает документы с полосами"
    assert ticket.priority == Ticket.Priority.HIGH


@pytest.mark.django_db
def test_ticket_delete(
    authenticated_client,
    ticket,
):
    """
    Авторизованный пользователь может удалить заявку.
    """
    ticket_id = ticket.pk

    response = authenticated_client.post(
        reverse("ticket_delete", kwargs={"pk": ticket.pk})
    )

    assert response.status_code == 302
    assert not Ticket.objects.filter(pk=ticket_id).exists()


@pytest.mark.django_db
def test_ticket_search_by_title(
    authenticated_client,
    ticket,
):
    """
    Поиск находит заявку по части заголовка.
    """
    response = authenticated_client.get(
        reverse("ticket_list"),
        {"search": "принтер"},
    )

    assert response.status_code == 200
    assert ticket.title in response.content.decode()


@pytest.mark.django_db
def test_ticket_search_excludes_unsuitable_ticket(
    authenticated_client,
    ticket,
):
    """
    Поиск не выводит заявку, которая не соответствует запросу.
    """
    response = authenticated_client.get(
        reverse("ticket_list"),
        {"search": "телефон"},
    )

    assert response.status_code == 200
    assert ticket.title not in response.content.decode()


@pytest.mark.django_db
def test_ticket_filter_by_status(
    authenticated_client,
    ticket,
):
    """
    Фильтр выводит заявки с выбранным статусом.
    """
    response = authenticated_client.get(
        reverse("ticket_list"),
        {"status": Ticket.Status.NEW},
    )

    assert response.status_code == 200
    assert ticket.title in response.content.decode()


@pytest.mark.django_db
def test_ticket_filter_by_priority(
    authenticated_client,
    ticket,
):
    """
    Фильтр выводит заявки с выбранным приоритетом.
    """
    response = authenticated_client.get(
        reverse("ticket_list"),
        {"priority": Ticket.Priority.MEDIUM},
    )

    assert response.status_code == 200
    assert ticket.title in response.content.decode()


@pytest.mark.django_db
def test_ticket_list_pagination(
    authenticated_client,
    user,
):
    """
    Список заявок разбивается на страницы по десять заявок.
    """
    for number in range(11):
        Ticket.objects.create(
            title=f"Тестовая заявка {number}",
            description="Описание тестовой заявки",
            category=Ticket.Category.PRINTER,
            priority=Ticket.Priority.MEDIUM,
            status=Ticket.Status.NEW,
            author=user,
        )

    response = authenticated_client.get(reverse("ticket_list"))

    assert response.status_code == 200
    assert response.context["is_paginated"] is True
    assert len(response.context["tickets"]) == 10

    second_page_response = authenticated_client.get(
        reverse("ticket_list"),
        {"page": 2},
    )

    assert second_page_response.status_code == 200
    assert len(second_page_response.context["tickets"]) == 1


@pytest.mark.django_db
def test_employee_can_set_waiting_status(
    client,
    employee_user,
    ticket,
):
    """
    Обычный сотрудник может перевести
    собственную заявку в статус «Ожидает уточнения».
    """
    ticket.author = employee_user
    ticket.save(update_fields=["author"])

    client.force_login(employee_user)

    response = client.post(
        reverse(
            "ticket_update",
            kwargs={"pk": ticket.pk},
        ),
        data={
            "title": ticket.title,
            "description": ticket.description,
            "category": ticket.category,
            "priority": ticket.priority,
            "status": Ticket.Status.WAITING,
        },
    )

    ticket.refresh_from_db()

    assert response.status_code == 302
    assert ticket.status == Ticket.Status.WAITING
