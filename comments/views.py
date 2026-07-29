from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView

from comments.models import Comment
from comments.serializers import CommentSerializer
from comments.forms import CommentForm
from tickets.models import Ticket


@extend_schema(
    tags=["comments"],
    summary="Управление комментариями",
    description="CRUD-операции для комментариев к заявкам технической поддержки.",
)
class CommentViewSet(ModelViewSet):
    """ViewSet для работы с комментариями."""

    queryset = Comment.objects.all().order_by("created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Веб-представление для добавления комментария к заявке.
    """

    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        """
        Получает заявку из адреса страницы.
        """
        self.ticket = get_object_or_404(
            Ticket,
            pk=self.kwargs["ticket_pk"],
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Автоматически сохраняет автора и заявку комментария.
        """
        form.instance.author = self.request.user
        form.instance.ticket = self.ticket

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        При ошибке снова показывает страницу заявки
        вместе с заполненной формой и сообщениями об ошибках.
        """
        return render(
            self.request,
            "tickets/ticket_detail.html",
            {
                "ticket": self.ticket,
                "comment_form": form,
            },
            status=400,
        )

    def get_success_url(self):
        """
        После добавления комментария возвращает пользователя
        на страницу заявки.
        """
        return reverse(
            "ticket_detail",
            kwargs={"pk": self.ticket.pk},
        )
