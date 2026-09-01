from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.serial_number})"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Aperto'),
        ('IN_PROGRESS', 'In lavorazione'),
        ('CLOSED', 'Chiuso'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Bassa'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='tickets')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_opened')
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assigned')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expected_close_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("view_manager_dashboard", "Può vedere la dashboard manager"),
        ]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"

    def clean(self):
        if self.expected_close_date and self.expected_close_date < timezone.now().date():
            raise ValidationError("La data prevista di chiusura non può essere nel passato.")
        if self.status == 'CLOSED' and self.technician is None:
            raise ValidationError("Un ticket chiuso deve avere un tecnico assegnato.")
