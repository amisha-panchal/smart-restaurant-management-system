from django.db import models
from menu.models import MenuItem


class Cart(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return sum(
            item.subtotal
            for item in self.items.all()
        )

    def __str__(self):
        return f"Cart #{self.id}"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"