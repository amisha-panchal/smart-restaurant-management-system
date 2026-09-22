from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from orders.models import Order, OrderItem
from employees.models import Employee
from reservations.models import Reservation
from inventory.models import InventoryItem
from openpyxl import Workbook
from django.http import HttpResponse
import json
from collections import Counter
import matplotlib.pyplot as plt
from reportlab.lib.utils import ImageReader
import io
from reportlab.lib import colors
from django.shortcuts import render, redirect

def reports_dashboard(request):
     
    if request.user.role != "manager":
        return redirect("home")


    total_orders = Order.objects.count()

    total_revenue = sum(
        order.total_amount
        for order in Order.objects.all()
    )

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    preparing_orders = Order.objects.filter(
        status='Preparing'
    ).count()

    served_orders = Order.objects.filter(
        status='Served'
    ).count()

    total_employees = Employee.objects.count()

    total_reservations = Reservation.objects.count()

    low_stock_items = InventoryItem.objects.filter(
        quantity__lte=10
    )

    recent_orders = Order.objects.order_by(
        '-created_at'
    )[:5]

    employees = Employee.objects.all()

    # Top Selling Foods

    top_foods = {}

    for item in OrderItem.objects.all():

        food_name = item.menu_item.name

        if food_name not in top_foods:
            top_foods[food_name] = 0

        top_foods[food_name] += item.quantity

    top_foods = sorted(
        top_foods.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # Chart Data

    status_data = Counter(
        Order.objects.values_list(
            'status',
            flat=True
        )
    )

    status_labels = list(
        status_data.keys()
    )

    status_counts = list(
        status_data.values()
    )

    food_labels = [
        food[0]
        for food in top_foods
    ]

    food_counts = [
        food[1]
        for food in top_foods
    ]

    context = {

        'total_orders': total_orders,
        'total_revenue': total_revenue,

        'pending_orders': pending_orders,
        'preparing_orders': preparing_orders,
        'served_orders': served_orders,

        'total_employees': total_employees,
        'total_reservations': total_reservations,

        'low_stock_items': low_stock_items,
        'recent_orders': recent_orders,
        'employees': employees,

        'top_foods': top_foods,

        # Charts

        'status_labels': json.dumps(
            status_labels
        ),

        'status_counts': json.dumps(
            status_counts
        ),

        'food_labels': json.dumps(
            food_labels
        ),

        'food_counts': json.dumps(
            food_counts
        ),
    }

    return render(
        request,
        'reports/reports.html',
        context
    )

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from datetime import datetime

from orders.models import Order, OrderItem
from employees.models import Employee
from reservations.models import Reservation

def export_pdf(request):
    
    if request.user.role != "manager":
        return redirect("home")


    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="restaurant_report.pdf"'

    pdf = canvas.Canvas(response)

    # =====================
    # DATA
    # =====================

    total_orders = Order.objects.count()

    total_revenue = sum(
        order.total_amount
        for order in Order.objects.all()
    )

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    preparing_orders = Order.objects.filter(
        status='Preparing'
    ).count()

    served_orders = Order.objects.filter(
        status='Served'
    ).count()

    total_employees = Employee.objects.count()

    total_reservations = Reservation.objects.count()

    # =====================
    # COVER PAGE
    # =====================

    pdf.setFillColor(
        colors.HexColor("#0F172A")
    )

    pdf.rect(
        0, 730, 700, 120,
        fill=1
    )

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        28
    )

    pdf.drawCentredString(
        300,
        790,
        "SMART RESTAURANT"
    )

    pdf.drawCentredString(
        300,
        755,
        "MANAGEMENT SYSTEM"
    )

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawCentredString(
        300,
        620,
        "Restaurant Analytics Report"
    )

    pdf.setFont(
        "Helvetica",
        14
    )

    pdf.drawCentredString(
        300,
        580,
        f"Generated On : {datetime.now().strftime('%d-%m-%Y %H:%M')}"
    )

    pdf.showPage()

    # =====================
    # DASHBOARD PAGE
    # =====================

    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawString(
        40,
        800,
        "Restaurant Business Dashboard"
    )

    # Orders

    pdf.setFillColor(
        colors.HexColor("#3B82F6")
    )

    pdf.roundRect(
        40, 620, 230, 120, 15,
        fill=1
    )

    pdf.setFillColor(colors.white)

    pdf.drawString(
        60,
        690,
        "TOTAL ORDERS"
    )

    pdf.setFont(
        "Helvetica-Bold",
        34
    )

    pdf.drawString(
        60,
        645,
        str(total_orders)
    )

    # Revenue

    pdf.setFillColor(
        colors.HexColor("#10B981")
    )

    pdf.roundRect(
        320, 620, 230, 120, 15,
        fill=1
    )

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        340,
        690,
        "TOTAL REVENUE"
    )

    pdf.drawString(
        340,
        645,
        f"₹ {total_revenue}"
    )

    # Employees

    pdf.setFillColor(
        colors.HexColor("#F59E0B")
    )

    pdf.roundRect(
        40, 450, 230, 120, 15,
        fill=1
    )

    pdf.setFillColor(colors.white)

    pdf.drawString(
        60,
        520,
        "EMPLOYEES"
    )

    pdf.drawString(
        60,
        475,
        str(total_employees)
    )

    # Reservations

    pdf.setFillColor(
        colors.HexColor("#EF4444")
    )

    pdf.roundRect(
        320, 450, 230, 120, 15,
        fill=1
    )

    pdf.setFillColor(colors.white)

    pdf.drawString(
        340,
        520,
        "RESERVATIONS"
    )

    pdf.drawString(
        340,
        475,
        str(total_reservations)
    )

    pdf.showPage()

    # =====================
    # ORDER STATUS PIE CHART
    # =====================

    status_labels = [
        "Pending",
        "Preparing",
        "Served"
    ]

    status_counts = [
        pending_orders,
        preparing_orders,
        served_orders
    ]

    plt.figure(figsize=(7, 5))

    plt.pie(
        status_counts,
        labels=status_labels,
        autopct='%1.1f%%'
    )

    plt.title(
        "Order Status Distribution"
    )

    buffer = io.BytesIO()

    plt.savefig(
        buffer,
        format='png',
        bbox_inches='tight'
    )

    plt.close()

    buffer.seek(0)

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        130,
        800,
        "Order Status Analysis"
    )

    pdf.drawImage(
        ImageReader(buffer),
        70,
        260,
        width=450,
        height=450
    )

    pdf.showPage()

    # =====================
    # TOP SELLING FOODS
    # =====================

    top_foods = {}

    for item in OrderItem.objects.all():

        food_name = item.menu_item.name

        if food_name not in top_foods:
            top_foods[food_name] = 0

        top_foods[food_name] += item.quantity

    top_foods = sorted(
        top_foods.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    food_names = [
        food[0]
        for food in top_foods
    ]

    food_qty = [
        food[1]
        for food in top_foods
    ]

    plt.figure(figsize=(8, 5))

    plt.barh(
        food_names,
        food_qty
    )

    plt.title(
        "Top Selling Foods"
    )

    plt.tight_layout()

    buffer2 = io.BytesIO()

    plt.savefig(
        buffer2,
        format='png',
        bbox_inches='tight'
    )

    plt.close()

    buffer2.seek(0)

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        150,
        800,
        "Top Selling Foods"
    )

    pdf.drawImage(
        ImageReader(buffer2),
        60,
        260,
        width=480,
        height=420
    )

    pdf.save()

    return response
def export_excel(request):
    
    if request.user.role != "manager":
        return redirect("home")


    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Restaurant Report"

    sheet.append([
        "Restaurant Analytics Report"
    ])

    sheet.append([])

    sheet.append([
        "Generated On",
        datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )
    ])

    sheet.append([])

    sheet.append([
        "Total Orders",
        Order.objects.count()
    ])

    sheet.append([
        "Total Revenue",
        float(
            sum(
                order.total_amount
                for order in Order.objects.all()
            )
        )
    ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="restaurant_report.xlsx"'

    workbook.save(response)

    return response