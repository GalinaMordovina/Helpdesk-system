from django.contrib import admin

from comments.models import Comment
from tickets.models import Ticket


@admin.action(description="Перевести выбранные заявки в статус «В работе»")
def mark_in_progress(modeladmin, request, queryset):
    """Перевод выбранных заявок в статус 'В работе'."""
    queryset.update(status=Ticket.Status.IN_PROGRESS)


@admin.action(description="Перевести выбранные заявки в статус «Ожидает уточнения»")
def mark_waiting(modeladmin, request, queryset):
    """Перевод выбранных заявок в статус 'Ожидает уточнения'."""
    queryset.update(status=Ticket.Status.WAITING)


@admin.action(description="Перевести выбранные заявки в статус «Выполнена»")
def mark_resolved(modeladmin, request, queryset):
    """Перевод выбранных заявок в статус 'Выполнена'."""
    queryset.update(status=Ticket.Status.RESOLVED)


@admin.action(description="Закрыть выбранные заявки")
def mark_closed(modeladmin, request, queryset):
    """Перевод выбранных заявок в статус 'Закрыта'."""
    queryset.update(status=Ticket.Status.CLOSED)


class CommentInline(admin.TabularInline):
    """Комментарии внутри карточки заявки."""

    model = Comment
    extra = 0

    fields = (
        "author",
        "text",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Настройка отображения модели Ticket в административной панели."""

    # Поля, отображаемые в списке заявок
    list_display = (
        "id",
        "title",
        "category",
        "priority",
        "status",
        "author",
        "assigned_to",
        "created_at",
        "updated_at",
    )

    # Фильтры справа
    list_filter = (
        "status",
        "priority",
        "category",
        "assigned_to",
        "author",
        "created_at",
    )

    # Поиск
    search_fields = (
        "title",
        "description",
        "author__username",
        "author__email",
        "assigned_to__username",
        "assigned_to__email",
    )

    # Сортировка по умолчанию
    ordering = ("-created_at",)

    # Навигация по датам
    date_hierarchy = "created_at"

    # Комментарии внутри карточки заявки
    inlines = (
        CommentInline,
    )

    # Массовые действия
    actions = (
        mark_in_progress,
        mark_waiting,
        mark_resolved,
        mark_closed,
    )
