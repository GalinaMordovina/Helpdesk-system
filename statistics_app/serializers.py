from rest_framework import serializers


class StatisticsSerializer(serializers.Serializer):
    total_tickets = serializers.IntegerField()
    open_tickets = serializers.IntegerField()
    closed_tickets = serializers.IntegerField()
    critical_tickets = serializers.IntegerField()
    by_status = serializers.DictField()
    by_priority = serializers.DictField()
    by_category = serializers.DictField()
