import pytest
from users.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_returns_200(client):
    """
    Проверяет, что главная страница успешно открывается.
    """

    response = client.get(reverse("home"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_home_page_uses_template(client):
    """
    Проверяет, что используется шаблон home.html.
    """

    response = client.get(reverse("home"))

    templates = [template.name for template in response.templates]

    assert "home.html" in templates


@pytest.mark.django_db
def test_home_page_contains_project_name(client):
    """
    Проверяет, что на странице отображается название проекта.
    """

    response = client.get(reverse("home"))

    assert "HelpDesk System" in response.content.decode()


@pytest.mark.django_db
def test_home_page_contains_authorization(client):
    """
    Проверяет, что отображается ссылка авторизации.
    """

    response = client.get(reverse("home"))

    assert "Авторизация" in response.content.decode()


@pytest.mark.django_db
def test_login_page_returns_200(client):
    """
    Проверяет, что страница входа успешно открывается.
    """

    response = client.get(reverse("login"))

    assert response.status_code == 200
    assert "registration/login.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_user_can_login(client):
    """
    Проверяет, что пользователь может войти в систему.
    """

    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123",
        role="employee",
    )

    response = client.post(
        reverse("login"),
        {
            "username": "testuser",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("home")


@pytest.mark.django_db
def test_authenticated_user_displayed(client):
    """
    Проверяет отображение имени авторизованного пользователя.
    """

    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123",
        role="employee",
    )

    client.login(
        username="testuser",
        password="testpassword123",
    )

    response = client.get(reverse("home"))

    assert "testuser" in response.content.decode()


@pytest.mark.django_db
def test_user_can_logout(client):
    """
    Проверяет, что пользователь может выйти из системы.
    """

    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123",
        role="employee",
    )

    client.login(
        username="testuser",
        password="testpassword123",
    )

    response = client.post(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("home")
