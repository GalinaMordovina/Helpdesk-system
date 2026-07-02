from django.conf import settings
from django.core.mail import send_mail


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


def send_notification(subject: str, message: str, recipient: str) -> None:
    """Универсальная отправка email."""

    if not recipient:
        return

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )


def send_ticket_created_email(manager_email: str, ticket) -> None:
    """Уведомление менеджеру о новой заявке."""

    subject = f"HelpDesk System - новая заявка #{ticket.id}"

    message = (
        "Здравствуйте!\n\n"
        "В системе зарегистрирована новая заявка.\n\n"
        f"Номер: #{ticket.id}\n"
        f"Тема: {ticket.title}\n"
        f"Автор: {ticket.author.username}\n"
        f"Категория: {ticket.get_category_display()}\n"
        f"Приоритет: {ticket.get_priority_display()}\n"
        f"Статус: {ticket.get_status_display()}\n\n"
        "Необходимо назначить исполнителя."
    )

    send_notification(subject, message, manager_email)
