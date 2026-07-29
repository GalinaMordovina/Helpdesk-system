import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from comments.models import Comment
from tickets.models import Ticket


User = get_user_model()


@pytest.fixture
def user(db):
    """
    Создаёт пользователя для проверки комментариев.
    """
    return User.objects.create_user(
        username="comment_user",
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


@pytest.fixture
def comment(ticket, user):
    """
    Создаёт комментарий к заявке.
    """
    return Comment.objects.create(
        ticket=ticket,
        author=user,
        text="Проверен кабель подключения.",
    )


@pytest.mark.django_db
def test_ticket_detail_displays_comment(
    authenticated_client,
    ticket,
    comment,
):
    """
    Комментарий отображается на странице заявки.
    """
    response = authenticated_client.get(
        reverse("ticket_detail", kwargs={"pk": ticket.pk})
    )

    assert response.status_code == 200
    assert comment.text in response.content.decode()
    assert comment.author.username in response.content.decode()


@pytest.mark.django_db
def test_ticket_detail_displays_comment_form(
    authenticated_client,
    ticket,
):
    """
    На странице заявки отображается форма комментария.
    """
    response = authenticated_client.get(
        reverse("ticket_detail", kwargs={"pk": ticket.pk})
    )

    assert response.status_code == 200
    assert "comment_form" in response.context
    assert 'name="text"' in response.content.decode()


@pytest.mark.django_db
def test_comment_create(
    authenticated_client,
    ticket,
    user,
):
    """
    Авторизованный пользователь может добавить комментарий.
    """
    response = authenticated_client.post(
        reverse(
            "comment_create",
            kwargs={"ticket_pk": ticket.pk},
        ),
        data={
            "text": "Проблема передана специалисту.",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "ticket_detail",
        kwargs={"pk": ticket.pk},
    )

    comment = Comment.objects.get(
        ticket=ticket,
        text="Проблема передана специалисту.",
    )

    assert comment.author == user


@pytest.mark.django_db
def test_empty_comment_is_not_created(
    authenticated_client,
    ticket,
):
    """
    Пустой комментарий не сохраняется.
    """
    response = authenticated_client.post(
        reverse(
            "comment_create",
            kwargs={"ticket_pk": ticket.pk},
        ),
        data={
            "text": "",
        },
    )

    assert response.status_code == 400
    assert Comment.objects.count() == 0
    assert "Обязательное поле" in response.content.decode()


@pytest.mark.django_db
def test_comment_create_requires_authentication(
    client,
    ticket,
):
    """
    Неавторизованный пользователь не может добавить комментарий.
    """
    response = client.post(
        reverse(
            "comment_create",
            kwargs={"ticket_pk": ticket.pk},
        ),
        data={
            "text": "Комментарий не должен сохраниться.",
        },
    )

    assert response.status_code == 302
    assert reverse("login") in response.url
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_comment_is_connected_to_correct_ticket(
    authenticated_client,
    user,
):
    """
    Комментарий сохраняется у заявки из адреса страницы.
    """
    first_ticket = Ticket.objects.create(
        title="Первая заявка",
        description="Описание первой заявки",
        category=Ticket.Category.PRINTER,
        priority=Ticket.Priority.MEDIUM,
        status=Ticket.Status.NEW,
        author=user,
    )

    second_ticket = Ticket.objects.create(
        title="Вторая заявка",
        description="Описание второй заявки",
        category=Ticket.Category.PRINTER,
        priority=Ticket.Priority.MEDIUM,
        status=Ticket.Status.NEW,
        author=user,
    )

    authenticated_client.post(
        reverse(
            "comment_create",
            kwargs={"ticket_pk": second_ticket.pk},
        ),
        data={
            "text": "Комментарий ко второй заявке.",
        },
    )

    comment = Comment.objects.get(
        text="Комментарий ко второй заявке.",
    )

    assert comment.ticket == second_ticket
    assert comment.ticket != first_ticket


@pytest.fixture
def employee(db):
    """
    Создаёт обычного пользователя.
    """
    return User.objects.create_user(
        username="employee_user",
        password="testpassword123",
        role="employee",
    )


@pytest.fixture
def support(db):
    """
    Создаёт специалиста технической поддержки.
    """
    return User.objects.create_user(
        username="support_user",
        password="testpassword123",
        role="support",
    )


@pytest.fixture
def manager(db):
    """
    Создаёт руководителя.
    """
    return User.objects.create_user(
        username="manager_user",
        password="testpassword123",
        role="manager",
    )


@pytest.mark.django_db
def test_employee_does_not_see_status_field(
    client,
    employee,
    ticket,
):
    """
    Обычный пользователь не видит поле статуса
    в форме редактирования заявки.
    """
    client.force_login(employee)

    response = client.get(
        reverse(
            "ticket_update",
            kwargs={"pk": ticket.pk},
        )
    )

    assert response.status_code == 200
    assert "status" not in response.context["form"].fields
    assert 'name="status"' not in response.content.decode()


@pytest.mark.django_db
def test_support_sees_status_field(
    client,
    support,
    ticket,
):
    """
    Специалист поддержки видит поле статуса
    в форме редактирования заявки.
    """
    client.force_login(support)

    response = client.get(
        reverse(
            "ticket_update",
            kwargs={"pk": ticket.pk},
        )
    )

    assert response.status_code == 200
    assert "status" in response.context["form"].fields
    assert 'name="status"' in response.content.decode()


@pytest.mark.django_db
def test_manager_sees_status_field(
    client,
    manager,
    ticket,
):
    """
    Руководитель видит поле статуса
    в форме редактирования заявки.
    """
    client.force_login(manager)

    response = client.get(
        reverse(
            "ticket_update",
            kwargs={"pk": ticket.pk},
        )
    )

    assert response.status_code == 200
    assert "status" in response.context["form"].fields
    assert 'name="status"' in response.content.decode()


@pytest.mark.django_db
def test_employee_cannot_change_ticket_status(
    client,
    employee,
    ticket,
):
    """
    Обычный пользователь не может изменить статус заявки,
    даже если вручную передаст его в POST-запросе.
    """
    client.force_login(employee)

    original_status = ticket.status

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
            "status": Ticket.Status.CLOSED,
        },
    )

    assert response.status_code == 302

    ticket.refresh_from_db()

    assert ticket.status == original_status


@pytest.mark.django_db
def test_support_can_change_ticket_status(
    client,
    support,
    ticket,
):
    """
    Специалист поддержки может изменить статус заявки.
    """
    client.force_login(support)

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
            "status": Ticket.Status.IN_PROGRESS,
        },
    )

    assert response.status_code == 302

    ticket.refresh_from_db()

    assert ticket.status == Ticket.Status.IN_PROGRESS
