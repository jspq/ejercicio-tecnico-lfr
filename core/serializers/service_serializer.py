from rest_framework import serializers
from core.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'pickup_address', 'driver', 'status', 'estimated_arrival_time', 'completed_at', 'driver_name']
        read_only_fields = ['id', 'driver']

    def get_driver_name(self, obj):
        if obj.driver:
            return obj.driver.name
        return None

    def validate_status(self, value):
        if value not in dict(Service.STATUS_CHOICES).keys():
            raise serializers.ValidationError(f"{value} status no es valido.")
        return value

    def validate_estimated_arrival_time(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("El tiempo estimado debe ser un valor entero.")
        return value