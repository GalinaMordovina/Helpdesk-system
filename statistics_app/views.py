from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import Ticket


@extend_schema(
    tags=["statistics"],
    summary="Статистика по заявкам",
    description=(
        "Аналитический endpoint системы технической поддержки. "
        "Возвращает общее количество заявок, количество открытых и закрытых заявок, "
        "число критических заявок, а также распределение заявок "
        "по статусам, приоритетам и категориям."
    ),
)
class StatisticsView(APIView):
    """Представление статистики по заявкам."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        _ = request

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

        by_status = dict(
            Ticket.objects.values("status")
            .annotate(count=Count("id"))
            .values_list("status", "count")
        )

        by_priority = dict(
            Ticket.objects.values("priority")
            .annotate(count=Count("id"))
            .values_list("priority", "count")
        )

        by_category = dict(
            Ticket.objects.values("category")
            .annotate(count=Count("id"))
            .values_list("category", "count")
        )

        return Response(
            {
                "total_tickets": total_tickets,
                "open_tickets": open_tickets,
                "closed_tickets": closed_tickets,
                "critical_tickets": critical_tickets,
                "by_status": by_status,
                "by_priority": by_priority,
                "by_category": by_category,
            }
        )
