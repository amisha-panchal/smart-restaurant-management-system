from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import PasswordResetHistory

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    def reset_count(self, obj):
        return obj.passwordresethistory_set.count()

    reset_count.short_description = 'Password Resets'

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'reset_count',
        'is_active',
    )

    list_filter = (
        'role',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Role Information',
            {
                'fields': ('role',)
            }
        ),
    )
@admin.register(PasswordResetHistory)
class PasswordResetHistoryAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'reset_time',
        'ip_address',
        'success'
    )

    list_filter = (
        'success',
        'reset_time'
    )

    search_fields = (
        'user__username',
        'user__email'
    )