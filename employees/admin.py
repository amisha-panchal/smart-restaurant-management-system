from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'role',
        'phone',
        'email',
        'shift',
        'salary'
    )

    search_fields = (
        'name',
        'role'
    )

    list_filter = (
        'role',
        'shift'
    )