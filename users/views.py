from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Проверка работоспособности API."""

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        _ = request  # чтобы не висело предупреждения (в след ветке продолжу)
        return Response({"status": "ok"})


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
