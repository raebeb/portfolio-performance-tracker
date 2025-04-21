from rest_framework import serializers

class PortfolioSummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    total_value = serializers.FloatField()
    weights = serializers.DictField(child=serializers.FloatField())
