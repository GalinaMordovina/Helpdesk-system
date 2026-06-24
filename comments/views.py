from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from comments.models import Comment
from comments.serializers import CommentSerializer


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
