import pytest
from rest_framework.test import APIClient

from tickets.models import Ticket
from users.models import User


@pytest.fixture
def api_client():
    """DRF API-клиент для тестирования endpoint'ов."""

    return APIClient()


@pytest.fixture
def employee_user(db):
    """Тестовый сотрудник."""

    return User.objects.create_user(
        username="employee_test",
        email="employee@test.com",
        password="testpass123",
        role="employee",
    )


@pytest.fixture
def support_user(db):
    """Тестовый специалист технической поддержки."""

    return User.objects.create_user(
        username="support_test",
        email="support@test.com",
        password="testpass123",
        role="support",
    )


@pytest.fixture
def manager_user(db):
    """Тестовый менеджер."""

    return User.objects.create_user(
        username="manager_test",
        email="manager@test.com",
        password="testpass123",
        role="manager",
    )


@pytest.fixture
def ticket(db, employee_user, support_user):
    """Одна тестовая заявка."""

    return Ticket.objects.create(
        title="Тестовая заявка",
        description="Описание тестовой заявки",
        category=Ticket.Category.SOFTWARE,
        priority=Ticket.Priority.MEDIUM,
        status=Ticket.Status.NEW,
        author=employee_user,
        assigned_to=support_user,
    )


@pytest.fixture
def tickets(db, employee_user, support_user):
    """Набор тестовых заявок для проверки поиска, фильтрации и сортировки."""

    ticket_1 = Ticket.objects.create(
        title="Не работает Outlook",
        description="Ошибка при запуске почтового клиента.",
        category=Ticket.Category.SOFTWARE,
        priority=Ticket.Priority.HIGH,
        status=Ticket.Status.NEW,
        author=employee_user,
        assigned_to=None,
    )

    ticket_2 = Ticket.objects.create(
        title="Не печатает принтер",
        description="Документы не отправляются на печать.",
        category=Ticket.Category.PRINTER,
        priority=Ticket.Priority.MEDIUM,
        status=Ticket.Status.IN_PROGRESS,
        author=employee_user,
        assigned_to=support_user,
    )

    ticket_3 = Ticket.objects.create(
        title="Нет доступа к интернету",
        description="На рабочем месте отсутствует подключение к сети.",
        category=Ticket.Category.NETWORK,
        priority=Ticket.Priority.LOW,
        status=Ticket.Status.WAITING,
        author=employee_user,
        assigned_to=support_user,
    )

    ticket_4 = Ticket.objects.create(
        title="Ошибка охранной сигнализации",
        description="На панели охранной системы отображается ошибка.",
        category=Ticket.Category.SECURITY,
        priority=Ticket.Priority.CRITICAL,
        status=Ticket.Status.CLOSED,
        author=employee_user,
        assigned_to=support_user,
    )

    return [ticket_1, ticket_2, ticket_3, ticket_4]
