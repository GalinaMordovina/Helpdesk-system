from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """Модель заявки технической поддержки."""

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        WAITING = "waiting", "Ожидает уточнения"
        RESOLVED = "resolved", "Выполнена"
        CLOSED = "closed", "Закрыта"

    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Высокий"
        CRITICAL = "critical", "Критический"

    class Category(models.TextChoices):
        SOFTWARE = "software", "Программное обеспечение"
        HARDWARE = "hardware", "Компьютерное оборудование"
        NETWORK = "network", "Сеть и интернет"
        PRINTER = "printer", "Оргтехника и печать"
        ACCOUNT = "account", "Учетные записи и доступ"
        SECURITY = "security", "Охранно-пожарные системы"
        MAINTENANCE = "maintenance", "Техническое обслуживание"
        OTHER = "other", "Другое"

    title = models.CharField(
        max_length=255,
        verbose_name="Тема заявки",
    )
    description = models.TextField(
        verbose_name="Описание проблемы",
    )
    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name="Категория",
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="Приоритет",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets",
        verbose_name="Автор заявки",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        verbose_name="Исполнитель",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.id} — {self.title}"
