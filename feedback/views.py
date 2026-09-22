from django.shortcuts import render, redirect
from django.db.models import Avg

from .models import Feedback
from menu.models import MenuItem
from notifications.models import Notification


def feedback_list(request):

    feedbacks = Feedback.objects.select_related(
        'menu_item'
    ).order_by(
        '-created_at'
    )

    total_feedbacks = Feedback.objects.count()

    average_rating = Feedback.objects.aggregate(
        Avg('rating')
    )['rating__avg']

    context = {

        'feedbacks': feedbacks,

        'total_feedbacks': total_feedbacks,

        'average_rating': round(
            average_rating or 0,
            1
        )

    }

    return render(
        request,
        'feedback/feedback_list.html',
        context
    )


def add_feedback(request):

    if request.method == 'POST':

        menu_item = MenuItem.objects.get(
            id=request.POST.get(
                'menu_item'
            )
        )

        feedback = Feedback.objects.create(

            menu_item=menu_item,

            customer_name=request.POST.get(
                'customer_name'
            ),

            rating=request.POST.get(
                'rating'
            ),

            message=request.POST.get(
                'message'
            )

        )

        # Notification

        Notification.objects.create(
            title="⭐ New Feedback",
            message=f"{feedback.customer_name} rated {feedback.menu_item.name} {feedback.rating}/5 stars"
        )

        return redirect(
            'feedback_list'
        )

    menu_items = MenuItem.objects.filter(
        is_available=True
    )

    return render(
        request,
        'feedback/add_feedback.html',
        {
            'menu_items': menu_items
        }
    )