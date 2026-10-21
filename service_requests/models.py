from django.db import models
from django.contrib.auth.models import User


class ServiceRequestModel(models.Model):

    SERVICE_TYPES = [
        ('General Service', 'General Service'),
        ('Engine Repair', 'Engine Repair'),
        ('Brake Repair', 'Brake Repair'),
        ('Electrical', 'Electrical'),
        ('AC Repair', 'AC Repair'),
        ('Tyre Service', 'Tyre Service'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Inspection', 'Inspection'),
        ('Repairing', 'Repairing'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
    ]

    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=100)
    problem_description = models.TextField()
    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPES
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Requested'
    )
    service_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )

    def __str__(self):
        return f"{self.vehicle_number} - {self.service_type}"
