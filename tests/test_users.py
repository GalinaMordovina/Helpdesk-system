import pytest


@pytest.mark.django_db
def test_create_employee_user(employee_user):
    assert employee_user.username == "employee_test"
    assert employee_user.email == "employee@test.com"
    assert employee_user.role == "employee"
    assert employee_user.check_password("testpass123")


@pytest.mark.django_db
def test_create_support_user(support_user):
    assert support_user.role == "support"


@pytest.mark.django_db
def test_create_manager_user(manager_user):
    assert manager_user.role == "manager"
