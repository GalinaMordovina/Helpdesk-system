from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q, Case, When, Value, IntegerField
from django.views.generic import ListView

from users.serializers import CurrentUserSerializer
from tickets.models import Ticket
from users.models import User


@extend_schema(exclude=True)
class HealthCheckView(APIView):
    """Проверка работоспособности API."""

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        _ = request  # чтобы не висело предупреждения (в след ветке продолжу)
        return Response({"status": "ok"})


@extend_schema(
    tags=["users"],
    summary="Текущий пользователь",
    description=(
        "Возвращает информацию об авторизованном пользователе. "
        "Для доступа необходимо передать действующий JWT access-токен."
    ),
    responses=CurrentUserSerializer,
)
class CurrentUserView(APIView):
    """Получение информации о текущем пользователе."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        )


class EmployeeListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    ListView,
):
    """Отображение списка сотрудников и количества назначенных заявок."""

    model = User
    template_name = "users/employee_list.html"
    context_object_name = "employees"

    def test_func(self):
        """Разрешает просмотр страницы только менеджеру."""
        return self.request.user.role == "manager"

    def get_queryset(self):
        """
        Возвращает сотрудников со статистикой назначенных заявок.
        Пользователи сортируются в следующем порядке:
        менеджеры, специалисты, сотрудники.
        """
        active_statuses = [
            Ticket.Status.NEW,
            Ticket.Status.IN_PROGRESS,
            Ticket.Status.WAITING,
        ]

        return (
            User.objects
            .annotate(
                active_tickets_count=Count(
                    "assigned_tickets",
                    filter=Q(
                        assigned_tickets__status__in=active_statuses,
                    ),
                    distinct=True,
                ),
                total_tickets_count=Count(
                    "assigned_tickets",
                    distinct=True,
                ),
                role_order=Case(
                    When(
                        role="manager",
                        then=Value(1),
                    ),
                    When(
                        role="support",
                        then=Value(2),
                    ),
                    When(
                        role="employee",
                        then=Value(3),
                    ),
                    default=Value(4),
                    output_field=IntegerField(),
                ),
            )
            .order_by(
                "role_order",
                "last_name",
                "first_name",
                "username",
            )
        )
