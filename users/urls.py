from django.urls import path
from users.views import HealthCheckView, CurrentUserView


urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path("users/me/", CurrentUserView.as_view(), name="current-user"),
]
