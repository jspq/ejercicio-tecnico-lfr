from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Driver
from core.serializers.driver_serializer import DriverSerializer

class DriverViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer