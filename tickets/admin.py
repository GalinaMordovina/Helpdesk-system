from django.contrib import admin

from tickets.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "priority",
        "status",
        "author",
        "assigned_to",
        "created_at",
    )
    list_filter = (
        "category",
        "priority",
        "status",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "author__username",
        "assigned_to__username",
    )
