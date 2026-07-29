from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    """
    Форма создания комментария.
    """

    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Введите комментарий...",
                }
            ),
        }
