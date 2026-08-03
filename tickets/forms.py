from django import forms

from tickets.models import Ticket


class TicketForm(forms.ModelForm):
    """
    Форма создания и редактирования заявки в веб-интерфейсе.
    Статус новой заявки устанавливается автоматически,
    поэтому пользователь его не выбирает.
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


class EmployeeTicketUpdateForm(forms.ModelForm):
    """
    Форма редактирования заявки обычным сотрудником.
    Сотрудник может изменить данные заявки,
    сохранить текущий статус или перевести заявку
    в статус «Ожидает уточнения».
    """

    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "category",
            "priority",
            "status",
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
        }

    def __init__(self, *args, **kwargs):
        """
        Оставляет сотруднику текущий статус заявки
        и возможность выбрать статус «Ожидает уточнения».
        """
        super().__init__(*args, **kwargs)

        current_status = self.instance.status

        allowed_statuses = list(
            dict.fromkeys(
                [
                    current_status,
                    Ticket.Status.WAITING,
                ]
            )
        )

        status_labels = dict(Ticket.Status.choices)

        self.fields["status"].choices = [
            (status, status_labels[status])
            for status in allowed_statuses
        ]

    def clean_status(self):
        """
        Запрещает сотруднику передавать недоступный статус
        вручную через POST-запрос.
        """
        new_status = self.cleaned_data["status"]

        allowed_statuses = {
            self.instance.status,
            Ticket.Status.WAITING,
        }

        if new_status not in allowed_statuses:
            raise forms.ValidationError(
                "Вы можете оставить текущий статус "
                "или выбрать «Ожидает уточнения»."
            )

        return new_status


class TicketUpdateForm(forms.ModelForm):
    """
    Форма редактирования заявки специалистом или менеджером.

    Позволяет изменять все данные заявки,
    выбирать статус и назначать исполнителя.
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
