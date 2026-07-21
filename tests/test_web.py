import pytest
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
