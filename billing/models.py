from django.db import models
from orders.models import Order


class Bill(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    gst = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Bill #{self.id}"