from rest_framework import viewsets
from core.models import Address
from core.serializers.address_serializer import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer