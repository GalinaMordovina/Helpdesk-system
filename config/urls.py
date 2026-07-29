from django.contrib import admin
from django.urls import path, include
from users.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView
from config.views import home
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path("", home, name="home"),

    path("accounts/", include("django.contrib.auth.urls")),
    path("tickets/", include("tickets.web_urls")),
    path("comments/", include("comments.web_urls")),

    path('admin/', admin.site.urls),

    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),

    # API
    path("api/", include("users.urls")),
    path("api/tickets/", include("tickets.urls")),
    path("api/comments/", include("comments.urls")),
    path("api/statistics/", include("statistics_app.urls")),

    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # ReDoc
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]


# в админке можно будет загружать файл и открывать его ссылкой (позже добавлю)
# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
