import django_filters

from tickets.models import Ticket


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """Фильтр для выбора нескольких текстовых значений."""


class TicketFilter(django_filters.FilterSet):
    """Фильтры для заявок."""

    status = CharInFilter(
        field_name="status",
        lookup_expr="in",
        help_text="Фильтр по нескольким статусам: new,in_progress,closed",
    )

    priority = CharInFilter(
        field_name="priority",
        lookup_expr="in",
        help_text="Фильтр по нескольким приоритетам: low,medium,high",
    )

    category = CharInFilter(
        field_name="category",
        lookup_expr="in",
        help_text="Фильтр по нескольким категориям: printer,network,software",
    )

    created_from = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        help_text="Дата создания от",
    )

    created_to = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        help_text="Дата создания до",
    )

    updated_from = django_filters.DateTimeFilter(
        field_name="updated_at",
        lookup_expr="gte",
        help_text="Дата обновления от",
    )

    updated_to = django_filters.DateTimeFilter(
        field_name="updated_at",
        lookup_expr="lte",
        help_text="Дата обновления до",
    )

    class Meta:
        model = Ticket
        fields = [
            "status",
            "priority",
            "category",
            "author",
            "assigned_to",
            "created_from",
            "created_to",
            "updated_from",
            "updated_to",
        ]
