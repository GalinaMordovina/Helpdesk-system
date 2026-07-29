from django import forms

from tickets.models import Ticket


class TicketForm(forms.ModelForm):
    """
    Форма создания и редактирования заявки
    в веб-интерфейсе.
    """

    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "category",
            "priority",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Кратко опишите проблему",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Подробно опишите проблему",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class TicketUpdateForm(forms.ModelForm):
    """
    Форма редактирования заявки.
    Позволяет изменять статус и назначать исполнителя.
    """

    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "category",
            "priority",
            "status",
            "assigned_to",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
