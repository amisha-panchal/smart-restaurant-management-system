from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
        ('chef', 'Chef'),
        ('waiter', 'Waiter'),
        ('customer', 'Customer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )

    def __str__(self):
        return self.username

class PasswordResetHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    reset_time = models.DateTimeField(
        auto_now_add=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    success = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.reset_time}"