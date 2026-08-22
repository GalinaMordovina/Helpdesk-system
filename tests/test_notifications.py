import pytest
from unittest.mock import patch

from notifications.services import (
    send_test_email,
    send_ticket_created_email,
    send_ticket_status_email,
)
from tickets.models import Ticket


@pytest.mark.django_db
@patch("notifications.services.send_mail")
def test_send_test_email(mock_send_mail):
    """Проверка отправки тестового письма."""

    send_test_email("test@example.com")

    mock_send_mail.assert_called_once()


@pytest.mark.django_db
@patch("notifications.services.send_mail")
def test_send_ticket_created_email_to_managers(mock_send_mail, ticket, manager_user):
    """Проверка уведомления менеджера о новой заявке."""

    send_ticket_created_email(ticket)

    mock_send_mail.assert_called_once()


@pytest.mark.django_db
@patch("notifications.services.send_mail")
def test_send_ticket_status_email_to_support(mock_send_mail, ticket, support_user):
    """Проверка уведомления специалиста при статусе 'В работе'."""

    ticket.status = Ticket.Status.IN_PROGRESS
    ticket.assigned_to = support_user
    ticket.save()

    send_ticket_status_email(ticket)

    mock_send_mail.assert_called_once()


@pytest.mark.django_db
@patch("notifications.services.send_mail")
def test_send_ticket_status_email_to_author_when_closed(mock_send_mail, ticket):
    """Проверка уведомления автора при закрытии заявки."""

    ticket.status = Ticket.Status.CLOSED
    ticket.save()

    send_ticket_status_email(ticket)

    mock_send_mail.assert_called_once()
