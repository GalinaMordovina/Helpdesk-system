from django.conf import settings
from django.core.mail import send_mail

from tickets.models import Ticket
from users.models import User


def send_test_email(recipient_email: str) -> None:
    """Отправляет тестовое email-уведомление."""

    send_mail(
        subject="HelpDesk System - тестовое уведомление",
        message=(
            "Здравствуйте!\n\n"
            "Это тестовое уведомление из системы HelpDesk System.\n\n"
            "Если вы получили это письмо, значит отправка email работает корректно."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )


def send_notification(subject: str, message: str, recipients: list[str]) -> None:
    """Универсальная отправка email."""

    if not recipients:
        return

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=False,
    )


def get_manager_emails() -> list[str]:
    """Возвращает список email всех менеджеров."""

    return list(
        User.objects.filter(role="manager")
        .exclude(email="")
        .values_list("email", flat=True)
    )


def build_ticket_message(ticket: Ticket, action_text: str) -> str:
    """Формирует текст письма по заявке."""

    assigned_to = ticket.assigned_to.username if ticket.assigned_to else "не назначен"

    return (
        "Здравствуйте!\n\n"
        f"{action_text}\n\n"
        f"Номер заявки: #{ticket.id}\n"
        f"Тема: {ticket.title}\n"
        f"Автор: {ticket.author.username}\n"
        f"Исполнитель: {assigned_to}\n"
        f"Категория: {ticket.get_category_display()}\n"
        f"Приоритет: {ticket.get_priority_display()}\n"
        f"Статус: {ticket.get_status_display()}\n\n"
        "HelpDesk System"
    )


def send_ticket_created_email(ticket: Ticket) -> None:
    """Уведомляет всех менеджеров о новой заявке."""

    manager_emails = get_manager_emails()

    send_notification(
        subject=f"HelpDesk System - новая заявка #{ticket.id}",
        message=build_ticket_message(
            ticket,
            "В системе зарегистрирована новая заявка. Необходимо назначить исполнителя.",
        ),
        recipients=manager_emails,
    )


def send_ticket_status_email(ticket: Ticket) -> None:
    """Отправляет уведомление в зависимости от текущего статуса заявки."""

    if ticket.status == Ticket.Status.NEW:
        recipients = get_manager_emails()
        action_text = "Заявка находится в статусе «Новая». Необходимо распределить работу."

    elif ticket.status == Ticket.Status.IN_PROGRESS:
        recipients = [ticket.assigned_to.email] if ticket.assigned_to and ticket.assigned_to.email else []
        action_text = "Вам назначена заявка. Необходимо приступить к выполнению."

    elif ticket.status == Ticket.Status.WAITING:
        recipients = get_manager_emails()
        action_text = "Заявка ожидает уточнения. Требуется вмешательство менеджера."

    elif ticket.status == Ticket.Status.RESOLVED:
        recipients = get_manager_emails()
        action_text = "Заявка переведена в статус «Выполнена». Необходимо проверить результат."

    elif ticket.status == Ticket.Status.CLOSED:
        recipients = [ticket.author.email] if ticket.author.email else []
        action_text = "Заявка закрыта. Работа по обращению завершена."

    else:
        return

    send_notification(
        subject=f"HelpDesk System - изменение статуса заявки #{ticket.id}",
        message=build_ticket_message(ticket, action_text),
        recipients=recipients,
    )
