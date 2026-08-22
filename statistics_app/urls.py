from django.urls import path

from statistics_app.views import StatisticsView

urlpatterns = [
    path("", StatisticsView.as_view(), name="statistics"),
]
