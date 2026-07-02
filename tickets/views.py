from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from tickets.models import Ticket
from tickets.serializers import TicketSerializer
from tickets.filters import TicketFilter
from notifications.services import send_ticket_created_email, send_ticket_status_email


@extend_schema(
    tags=["tickets"],
    summary="Управление заявками",
    description="CRUD-операции для заявок технической поддержки.",
    parameters=[
        OpenApiParameter(
            name="search",
            description="Поиск по теме и описанию заявки",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="status",
            description="Фильтр по статусам через запятую: new,in_progress,closed",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="priority",
            description="Фильтр по приоритетам через запятую: low,medium,high,critical",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="category",
            description="Фильтр по категориям через запятую: printer,network,software",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="created_from",
            description="Дата создания от. Формат: YYYY-MM-DDTHH:MM:SS",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="created_to",
            description="Дата создания до. Формат: YYYY-MM-DDTHH:MM:SS",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="ordering",
            description="Сортировка: created_at, -created_at, updated_at, -updated_at",
            required=False,
            type=str,
        ),
    ],
)
class TicketViewSet(ModelViewSet):
    """ViewSet для работы с заявками."""

    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = TicketFilter

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "priority",
        "status",
    ]

    ordering = ["-created_at"]

    def perform_create(self, serializer):
        ticket = serializer.save()
        send_ticket_created_email(ticket)


    def perform_update(self, serializer):
        ticket = serializer.save()
        send_ticket_status_email(ticket)

