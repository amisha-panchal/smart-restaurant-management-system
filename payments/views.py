from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.conf import settings
import razorpay

from orders.models import Order
from .models import Payment


def checkout(request, order_id):

    if request.user.role != "customer":
        return redirect("home")

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items",
            "items__menu_item"
        ),
        id=order_id
    )

    gst = round(
        float(order.total_amount) * 0.05,
        2
    )

    grand_total = round(
        float(order.total_amount) + gst,
        2
    )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    razorpay_order = client.order.create({
        "amount": int(grand_total * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    if request.method == "POST":

        Payment.objects.get_or_create(
            order=order,
            defaults={
                "customer": request.user,
                "amount": grand_total,
                "payment_method": "Razorpay",
                "status": "Paid"
            }
        )

        return redirect(
            "payment_success",
            order_id=order.id
        )

    return render(
        request,
        "payments/checkout.html",
        {
            "order": order,
            "gst": gst,
            "grand_total": grand_total,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": razorpay_order["id"]
        }
    )


def payment_history(request):

    if request.user.role not in [
        "manager",
        "cashier"
    ]:
        return redirect("home")

    payments = Payment.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "payments/payment_history.html",
        {
            "payments": payments
        }
    )


def payment_success(request, order_id):

    if request.user.role != "customer":
        return redirect("home")

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "payments/payment_success.html",
        {
            "order": order
        }
    )