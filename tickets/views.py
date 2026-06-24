from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from tickets.models import Ticket
from tickets.serializers import TicketSerializer


@extend_schema(
    tags=["tickets"],
    summary="Управление заявками",
    description="CRUD-операции для заявок технической поддержки.",
)
class TicketViewSet(ModelViewSet):
    """ViewSet для работы с заявками."""

    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter, OrderingFilter]

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

