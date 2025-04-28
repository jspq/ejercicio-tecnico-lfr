from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Address
from core.serializers.address_serializer import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer