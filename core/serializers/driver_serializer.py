from rest_framework import serializers
from core.models import Driver, Address

class DriverSerializer(serializers.ModelSerializer):
    current_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        model = Driver
        fields = '__all__'