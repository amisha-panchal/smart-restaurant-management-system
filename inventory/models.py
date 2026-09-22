from django.db import models


class InventoryItem(models.Model):

    name = models.CharField(
        max_length=100
    )

    quantity = models.PositiveIntegerField()

    unit = models.CharField(
        max_length=20,
        default="kg"
    )

    minimum_stock = models.PositiveIntegerField(
        default=10
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_low_stock(self):
        return self.quantity <= self.minimum_stock

    def __str__(self):
        return self.name