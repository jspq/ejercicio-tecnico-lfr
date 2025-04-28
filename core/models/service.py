from django.db import models
from core.models.address import Address
from core.models.driver import Driver
import uuid

class Service(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled'),
        ('ASSIGNED', 'Assigned'),
        ('COMPLETED', 'Completed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pickup_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='pickup_services')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    secret_code = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    estimated_arrival_time = models.IntegerField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Service {self.id} - {self.get_status_display()}"
