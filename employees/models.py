from django.db import models


class Employee(models.Model):

    ROLE_CHOICES = [
        ('Chef', 'Chef'),
        ('Waiter', 'Waiter'),
        ('Manager', 'Manager'),
        ('Cashier', 'Cashier'),
    ]

    SHIFT_CHOICES = [
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
        ('Night', 'Night'),
    ]

    name = models.CharField(max_length=100)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField()

    shift = models.CharField(
        max_length=20,
        choices=SHIFT_CHOICES
    )

    joining_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name