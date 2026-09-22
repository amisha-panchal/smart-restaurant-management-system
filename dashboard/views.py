from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.db.models import Sum
from django.http import HttpResponse
from django.http import HttpResponse

@login_required
def dashboard(request):
    raise Exception("TEST")

#  
# 
# @login_required
# def dashboard(request):
# 
#     total_orders = Order.objects.count()
# 
#     total_revenue = (
#         Order.objects.aggregate(
#             total=Sum('total_price')
#         )['total'] or 0
#     )
# 
#     recent_orders = Order.objects.order_by('-created_at')[:5]
# 
#     context = {
#         'total_orders': total_orders,
#         'total_revenue': total_revenue,
#         'recent_orders': recent_orders,
#         'total_reservations': 0,
#         'low_stock': 0,
#     }
# 
#     return render(
#         request,
#         'dashboard.html',
#         context
#     )