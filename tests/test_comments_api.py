import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_comments_list(api_client, manager_user):
    """Получение списка комментариев."""

    api_client.force_authenticate(user=manager_user)

    response = api_client.get("/api/comments/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_comment(api_client, employee_user, ticket):
    """Создание комментария через API."""

    api_client.force_authenticate(user=employee_user)

    payload = {
        "ticket": ticket.id,
        "author": employee_user.id,
        "text": "Комментарий через API",
    }

    response = api_client.post(
        "/api/comments/",
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == "Комментарий через API"


@pytest.mark.django_db
def test_update_comment(api_client, employee_user, ticket):
    """Редактирование комментария через API."""

    api_client.force_authenticate(user=employee_user)

    create_response = api_client.post(
        "/api/comments/",
        {
            "ticket": ticket.id,
            "author": employee_user.id,
            "text": "Старый текст",
        },
        format="json",
    )

    comment_id = create_response.data["id"]

    response = api_client.patch(
        f"/api/comments/{comment_id}/",
        {"text": "Новый текст"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["text"] == "Новый текст"


@pytest.mark.django_db
def test_delete_comment(api_client, manager_user, ticket):
    """Удаление комментария через API."""

    api_client.force_authenticate(user=manager_user)

    create_response = api_client.post(
        "/api/comments/",
        {
            "ticket": ticket.id,
            "author": manager_user.id,
            "text": "Комментарий для удаления",
        },
        format="json",
    )

    comment_id = create_response.data["id"]

    response = api_client.delete(f"/api/comments/{comment_id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
