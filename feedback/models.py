from django.db import models
from menu.models import MenuItem


class Feedback(models.Model):

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=100
    )

    rating = models.IntegerField()

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.menu_item:
            return f"{self.customer_name} - {self.menu_item.name}"

        return self.customer_name