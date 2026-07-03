from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@extend_schema(
    tags=["auth"],
    summary="Получение JWT-токена",
    description=(
        "Авторизация пользователя по логину и паролю. "
        "Возвращает access и refresh токены."
    ),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение пары JWT-токенов."""


@extend_schema(
    tags=["auth"],
    summary="Обновление access-токена",
    description=(
        "Обновляет access-токен по действующему refresh-токену. "
        "Используется, когда access-токен истёк."
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    """Обновление access-токена."""
