from django.db import models
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()


class Payment(models.Model):

    PAYMENT_METHODS = [
        ('COD', 'Cash On Delivery'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment #{self.id}"