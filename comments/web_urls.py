from django.urls import path

from comments.views import CommentCreateView


urlpatterns = [
    path(
        "ticket/<int:ticket_pk>/create/",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
]
