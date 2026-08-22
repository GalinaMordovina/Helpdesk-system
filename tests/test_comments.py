import pytest

from comments.models import Comment


@pytest.mark.django_db
def test_comment_creation(ticket, employee_user):
    """Создание комментария."""

    comment = Comment.objects.create(
        ticket=ticket,
        author=employee_user,
        text="Проблема подтверждена.",
    )

    assert comment.ticket == ticket
    assert comment.author == employee_user
    assert comment.text == "Проблема подтверждена."


@pytest.mark.django_db
def test_comment_string_representation(ticket, employee_user):
    """Строковое представление комментария."""

    comment = Comment.objects.create(
        ticket=ticket,
        author=employee_user,
        text="Комментарий",
    )

    assert str(comment) == f"Комментарий #{comment.id} к заявке #{ticket.id}"
