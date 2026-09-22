from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.db.models import Sum

from orders.models import Order
from .models import Bill
from django.http import HttpResponse

from reportlab.pdfgen import canvas


def bill_list(request):
    
    if request.user.role not in [
        "manager",
        "cashier",
        "admin"
    ]:
        return redirect("home")

    bills = Bill.objects.select_related(
        "order"
    ).order_by(
        "-created_at"
    )

    total_bills = bills.count()

    total_revenue = bills.aggregate(
        Sum("total_amount")
    )["total_amount__sum"] or 0

    total_gst = bills.aggregate(
        Sum("gst")
    )["gst__sum"] or 0

    context = {

        "bills": bills,

        "total_bills": total_bills,

        "total_revenue": round(
            total_revenue,
            2
        ),

        "total_gst": round(
            total_gst,
            2
        ),
    }

    return render(
        request,
        "billing/bill_list.html",
        context
    )


def generate_bill(request, order_id):
    
    
    if request.user.role not in [
        "manager",
        "cashier",
        "admin"
    ]:
        return redirect("home")

    order = get_object_or_404(
        Order,
        id=order_id
    )

    # Only Served orders can be billed
    if order.status != "Served":

        return redirect(
            "order_list"
        )

    # Prevent duplicate bills
    if Bill.objects.filter(
        order=order
    ).exists():

        return redirect(
            "bill_list"
        )

    subtotal = round(
        float(order.total_amount),
        2
    )

    gst = round(
        subtotal * 0.05,
        2
    )

    total_amount = round(
        subtotal + gst,
        2
    )

    Bill.objects.create(
        order=order,
        subtotal=subtotal,
        gst=gst,
        total_amount=total_amount
    )

    return redirect(
        "bill_list"
    )


def invoice_detail(request, bill_id):
    
    
    if request.user.role not in [
        "manager",
        "cashier",
        "admin"
    ]:
        return redirect("home")

    bill = get_object_or_404(
        Bill.objects.select_related(
            "order"
        ).prefetch_related(
            "order__items",
            "order__items__menu_item"
        ),
        id=bill_id
    )

    return render(
        request,
        "billing/invoice_detail.html",
        {
            "bill": bill
        }
    )
    
def download_invoice_pdf(request, bill_id):

    bill = get_object_or_404(
        Bill.objects.select_related(
            "order"
        ).prefetch_related(
            "order__items",
            "order__items__menu_item"
        ),
        id=bill_id
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="invoice_{bill.id}.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        50,
        800,
        "Smart Restaurant Invoice"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        50,
        770,
        f"Invoice ID: {bill.id}"
    )

    pdf.drawString(
        50,
        750,
        f"Order ID: {bill.order.id}"
    )

    pdf.drawString(
        50,
        730,
        f"Date: {bill.created_at.strftime('%d-%m-%Y %H:%M')}"
    )

    y = 680

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "Food Item"
    )

    pdf.drawString(
        250,
        y,
        "Qty"
    )

    pdf.drawString(
        350,
        y,
        "Price"
    )

    pdf.drawString(
        450,
        y,
        "Subtotal"
    )

    y -= 30

    pdf.setFont(
        "Helvetica",
        12
    )

    for item in bill.order.items.all():

        pdf.drawString(
            50,
            y,
            item.menu_item.name
        )

        pdf.drawString(
            250,
            y,
            str(item.quantity)
        )

        pdf.drawString(
            350,
            y,
            f"₹{item.menu_item.price}"
        )

        pdf.drawString(
            450,
            y,
            f"₹{item.subtotal}"
        )

        y -= 25

    y -= 20

    pdf.drawString(
        350,
        y,
        f"Subtotal: ₹{bill.subtotal}"
    )

    y -= 25

    pdf.drawString(
        350,
        y,
        f"GST (5%): ₹{bill.gst}"
    )

    y -= 25

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        350,
        y,
        f"Total: ₹{bill.total_amount}"
    )

    pdf.save()

    return response