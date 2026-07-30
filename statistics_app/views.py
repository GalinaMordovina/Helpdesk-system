from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)

from statistics_app.serializers import StatisticsSerializer
from statistics_app.services import get_ticket_statistics


@extend_schema(
    tags=["statistics"],
    summary="Статистика по заявкам",
    description=(
        "Аналитический endpoint системы технической поддержки. "
        "Возвращает общее количество заявок, количество открытых и закрытых заявок, "
        "число критических заявок, а также распределение заявок "
        "по статусам, приоритетам и категориям."
    ),
    responses=StatisticsSerializer,
)
class StatisticsView(APIView):
    """Представление статистики по заявкам."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращает статистику по заявкам."""

        statistics = get_ticket_statistics()

        return Response(statistics)


class StatisticsWebView(LoginRequiredMixin, UserPassesTestMixin, TemplateView,):
    """
    Представление статистики в веб-интерфейсе.
    Страница доступна специалистам поддержки
    и руководителям.
    """

    template_name = "statistics_app/statistics.html"

    def test_func(self):
        """
        Проверяет право пользователя на просмотр статистики.
        """

        return self.request.user.role in [
            "support",
            "manager",
        ]

    def get_context_data(self, **kwargs):
        """
        Добавляет статистику по заявкам в контекст шаблона.
        """

        context = super().get_context_data(**kwargs)
        context.update(get_ticket_statistics())

        return context
