from django.urls import path

from statistics_app.views import StatisticsWebView


urlpatterns = [
    path(
        "",
        StatisticsWebView.as_view(),
        name="statistics_web",
    ),
]
