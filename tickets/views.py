from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)

from tickets.models import Ticket
from tickets.serializers import TicketSerializer
from tickets.filters import TicketFilter
from notifications.services import send_ticket_created_email, send_ticket_status_email
from tickets.forms import TicketForm


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


class TicketListView(LoginRequiredMixin, ListView):
    """
    Представление списка заявок в веб-интерфейсе.
    """

    model = Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 10

    def get_queryset(self):
        """
        Возвращает список заявок с учётом поиска и фильтров.
        """

        queryset = Ticket.objects.select_related(
            "author",
            "assigned_to",
        ).order_by("-created_at")

        # Поиск по названию и описанию заявки
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
            )

        # Фильтр по статусу
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Фильтр по приоритету
        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляет в шаблон варианты статусов и приоритетов заявок.
        """

        context = super().get_context_data(**kwargs)

        context["ticket_statuses"] = Ticket.Status.choices
        context["ticket_priorities"] = Ticket.Priority.choices

        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    """
    Представление одной заявки в веб-интерфейсе.
    """

    model = Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

    def get_queryset(self):
        """
        Возвращает заявки для авторизованного пользователя.
        """

        return Ticket.objects.select_related(
            "author",
            "assigned_to",
        )


class TicketCreateView(LoginRequiredMixin, CreateView):
    """
    Представление создания заявки в веб-интерфейсе.
    """

    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"

    def form_valid(self, form):
        """
        Устанавливает текущего пользователя автором заявки
        и отправляет уведомление после создания.
        """

        form.instance.author = self.request.user

        response = super().form_valid(form)

        send_ticket_created_email(self.object)

        return response

    def get_success_url(self):
        """
        После создания открывает карточку новой заявки.
        """

        return reverse_lazy(
            "ticket_detail",
            kwargs={"pk": self.object.pk},
        )


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление редактирования заявки.
    """

    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"

    def get_success_url(self):
        """
        После сохранения открывает карточку заявки.
        """

        return reverse_lazy(
            "ticket_detail",
            kwargs={"pk": self.object.pk},
        )


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление удаления заявки.
    """

    model = Ticket
    template_name = "tickets/ticket_confirm_delete.html"
    success_url = reverse_lazy("ticket_list")
