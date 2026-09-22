from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Reservation
from notifications.models import Notification
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages



def create_reservation(request):

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name"
        )

        phone = request.POST.get(
            "phone"
        )

        guests = request.POST.get(
            "guests"
        )

        table_number = request.POST.get(
            "table_number"
        )

        reservation_time = request.POST.get(
            "reservation_time"
        )

        existing = Reservation.objects.filter(
            table_number=table_number,
            reservation_time=reservation_time,
            status__in=[
                "Booked",
                "Seated"
            ]
        ).exists()

        if existing:

            return render(
                request,
                "reservations/create_reservation.html",
                {
                    "error":
                    "This table is already reserved for that time."
                }
            )

        reservation = Reservation.objects.create(
            customer_name=customer_name,
            phone=phone,
            guests=guests,
            table_number=table_number,
            reservation_time=reservation_time
        )

        Notification.objects.create(
            title="📅 New Reservation",
            message=f"Table {reservation.table_number} booked by {reservation.customer_name}"
        )

        messages.success(
            request,
            "🎉 Your reservation has been confirmed successfully!"
        )

        return redirect(
            "home"
        )

    return render(
        request,
        "reservations/create_reservation.html"
    )


def reservation_list(request):

    reservations = Reservation.objects.all().order_by(
        "-reservation_time"
    )

    return render(
        request,
        "reservations/reservation_list.html",
        {
            "reservations": reservations
        }
    )


def update_reservation_status(
    request,
    reservation_id
):

    reservation = get_object_or_404(
        Reservation,
        id=reservation_id
    )

    if request.method == "POST":

        reservation.status = request.POST.get(
            "status"
        )

        reservation.save()

        Notification.objects.create(
            title="📅 Reservation Status Updated",
            message=f"Table {reservation.table_number} status changed to {reservation.status}"
        )

    return redirect(
        "reservation_list"
    )