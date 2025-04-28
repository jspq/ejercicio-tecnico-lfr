from django.db import models
from core.models.address import Address
from django.utils import timezone

class Driver(models.Model):
    name = models.CharField(max_length=255)
    vehicle_model = models.CharField(max_length=255)
    vehicle_color = models.CharField(max_length=255)
    license_plate = models.CharField(max_length=255)
    current_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name="drivers")
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name