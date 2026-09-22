from django.shortcuts import render
from .models import Notification


def notification_list(request):

    notifications = Notification.objects.order_by(
        '-created_at'
    )

    return render(
        request,
        'notifications/notifications.html',
        {
            'notifications': notifications
        }
    )