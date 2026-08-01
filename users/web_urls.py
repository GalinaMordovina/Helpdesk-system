from django.urls import path

from users.views import EmployeeListView


urlpatterns = [
    path(
        "",
        EmployeeListView.as_view(),
        name="employee_list",
    ),
]
