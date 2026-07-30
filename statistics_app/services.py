from django.db.models import Count

from tickets.models import Ticket


def get_ticket_statistics():
    """
    Возвращает общую статистику по заявкам.

    Функция используется как API-представлением,
    так и веб-страницей статистики.
    """

    total_tickets = Ticket.objects.count()

    open_tickets = Ticket.objects.exclude(
        status__in=[
            Ticket.Status.RESOLVED,
            Ticket.Status.CLOSED,
        ]
    ).count()

    closed_tickets = Ticket.objects.filter(
        status__in=[
            Ticket.Status.RESOLVED,
            Ticket.Status.CLOSED,
        ]
    ).count()

    critical_tickets = Ticket.objects.filter(
        priority=Ticket.Priority.CRITICAL
    ).count()

    status_counts = dict(
        Ticket.objects.values("status")
        .annotate(count=Count("id"))
        .values_list("status", "count")
    )

    by_status = [
        (
            label,
            status_counts.get(value, 0),
        )
        for value, label in Ticket.Status.choices
    ]

    priority_counts = dict(
        Ticket.objects.values("priority")
        .annotate(count=Count("id"))
        .values_list("priority", "count")
    )

    priority_labels = dict(Ticket.Priority.choices)

    priority_order = [
        Ticket.Priority.CRITICAL,
        Ticket.Priority.HIGH,
        Ticket.Priority.MEDIUM,
        Ticket.Priority.LOW,
    ]

    by_priority = [
        (
            priority_labels[value],
            priority_counts[value],
        )
        for value in priority_order
        if priority_counts.get(value, 0) > 0
    ]

    category_choices = dict(Ticket.Category.choices)

    by_category = {
        category_choices.get(category, category): count
        for category, count in (
            Ticket.objects.values("category")
            .annotate(count=Count("id"))
            .values_list("category", "count")
        )
    }

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "closed_tickets": closed_tickets,
        "critical_tickets": critical_tickets,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
    }
