import pytest

from tickets.models import Ticket


@pytest.mark.django_db
def test_ticket_creation(ticket):
    assert ticket.title == "Тестовая заявка"
    assert ticket.description == "Описание тестовой заявки"
    assert ticket.category == Ticket.Category.SOFTWARE
    assert ticket.priority == Ticket.Priority.MEDIUM
    assert ticket.status == Ticket.Status.NEW
    assert ticket.author.role == "employee"
    assert ticket.assigned_to.role == "support"


@pytest.mark.django_db
def test_ticket_string_representation(ticket):
    assert str(ticket) == f"#{ticket.id} — {ticket.title}"


@pytest.mark.django_db
def test_ticket_can_be_without_assignee(employee_user):
    ticket = Ticket.objects.create(
        title="Заявка без исполнителя",
        description="Исполнитель пока не назначен",
        category=Ticket.Category.NETWORK,
        priority=Ticket.Priority.HIGH,
        status=Ticket.Status.NEW,
        author=employee_user,
        assigned_to=None,
    )

    assert ticket.assigned_to is None
    assert ticket.status == Ticket.Status.NEW
