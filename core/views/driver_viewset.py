from rest_framework import viewsets
from core.models import Driver
from core.serializers.driver_serializer import DriverSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer