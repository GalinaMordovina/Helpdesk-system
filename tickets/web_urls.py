from django.urls import path

from tickets.views import (
    TicketListView,
    TicketDetailView,
    TicketCreateView,
    TicketUpdateView,
    TicketDeleteView,
)


urlpatterns = [
    path(
        "",
        TicketListView.as_view(),
        name="ticket_list",
    ),
    path(
        "create/",
        TicketCreateView.as_view(),
        name="ticket_create",
    ),
    path(
        "<int:pk>/",
        TicketDetailView.as_view(),
        name="ticket_detail",
    ),
    path(
        "<int:pk>/edit/",
        TicketUpdateView.as_view(),
        name="ticket_update",
    ),
    path(
        "<int:pk>/delete/",
        TicketDeleteView.as_view(),
        name="ticket_delete",
    ),
]
