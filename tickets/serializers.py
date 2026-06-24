from rest_framework import serializers

from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Сериализатор заявок."""

    class Meta:
        model = Ticket
        fields = "__all__"
