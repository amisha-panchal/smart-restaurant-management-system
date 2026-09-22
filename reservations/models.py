from django.db import models


class Reservation(models.Model):

    STATUS_CHOICES = [
        ("Booked", "Booked"),
        ("Seated", "Seated"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    customer_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    guests = models.PositiveIntegerField()

    table_number = models.PositiveIntegerField()

    reservation_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Booked"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-reservation_time"]

    def __str__(self):
        return (
            f"{self.customer_name} - "
            f"Table {self.table_number}"
        )