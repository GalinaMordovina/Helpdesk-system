from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path("api/", include("users.urls")),
    path("api/tickets/", include("tickets.urls")),
    path("api/comments/", include("comments.urls")),
]


# в админке можно будет загружать файл и открывать его ссылкой (позже добавлю)
# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
