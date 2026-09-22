from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from menu.models import MenuItem
from .models import Order, OrderItem
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from notifications.models import Notification


def create_order(request, item_id):

    item = get_object_or_404(
        MenuItem,
        id=item_id
    )

    if request.method == "POST":

        quantity = int(
            request.POST.get("quantity")
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            menu_item=item,
            quantity=quantity
        )

        return redirect(
            "order_list"
        )

    return render(
        request,
        "orders/create_order.html",
        {
            "item": item
        }
    )


def order_list(request):
    
    
    if request.user.role == "customer":
        return redirect("home")


    orders = Order.objects.prefetch_related(
        "items",
        "items__menu_item"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "orders/order_list.html",
        {
            "orders": orders
        }
    )

def update_order_status(
    request,
    order_id
):
    
    if request.user.role not in [
        "manager",
        "waiter",
        "chef"
    ]:
        return redirect("home")

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        order.status = request.POST.get(
            "status"
        )

        order.save()

        # Create Notification
        Notification.objects.create(
            title="📦 Order Status Updated",
            message=f"Order #{order.id} status changed to {order.status}"
        )

    return redirect(
        "manage_orders"
    )


def place_order(request):

    cart_id = request.session.get(
        "cart_id"
    )

    if not cart_id:
        return redirect(
            "cart"
        )

    try:

        cart = Cart.objects.get(
            id=cart_id
        )

    except Cart.DoesNotExist:

        return redirect(
            "cart"
        )

    # Create Order
    order = Order.objects.create(
        user=request.user,
        status="Pending"
    )

    # Create Notification
    Notification.objects.create(
        title="🔔 New Order",
        message=f"Order #{order.id} has been placed successfully"
    )

    # Move Cart Items → Order Items
    for cart_item in cart.items.all():

        OrderItem.objects.create(
            order=order,
            menu_item=cart_item.menu_item,
            quantity=cart_item.quantity
        )

    # Clear Cart
    cart.items.all().delete()
    cart.delete()

    request.session.pop(
        "cart_id",
        None
    )

    return redirect(
        "checkout",
        order_id=order.id
    )

    # Move Cart Items → Order Items
    for cart_item in cart.items.all():

        OrderItem.objects.create(
            order=order,
            menu_item=cart_item.menu_item,
            quantity=cart_item.quantity
        )

   # Clear Cart
    cart.items.all().delete()
    cart.delete()

    request.session.pop(
    "cart_id",
    None
)

    return redirect(
    "checkout",
    order_id=order.id
)
@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/order_history.html',
        {
            'orders': orders
        }
    )
def manage_orders(request):
    
    if request.user.role not in [
        "manager",
        "waiter",
        "chef"
    ]:
        return redirect("home")
    orders = Order.objects.all().order_by('-created_at')

    return render(
        request,
        'orders/manage_orders.html',
        {'orders': orders}
    )
# from django.shortcuts import render, redirect, get_object_or_404
# from menu.models import MenuItem
# from .models import Order, OrderItem
# 
# def create_order(request, item_id):
# 
#     item = get_object_or_404(MenuItem, id=item_id)
# 
#     if request.method == "POST":
# 
#         print("POST RECEIVED")
# 
#         quantity = int(request.POST.get("quantity"))
#         print("Quantity =", quantity)
# 
#         order = Order.objects.create()
#         print("Order Created =", order.id)
# 
#         OrderItem.objects.create(
#             order=order,
#             menu_item=item,
#             quantity=quantity
#         )
# 
#         print("OrderItem Created")
# 
#         return redirect("order_list")
# 
#     return render(
#         request,
#         "orders/create_order.html",
#         {"item": item}
#     )
# 
# 
# def order_list(request):
# 
#     orders = Order.objects.prefetch_related(
#         'items',
#         'items__menu_item'
#     ).order_by("-created_at")
# 
#     return render(
#         request,
#         "orders/order_list.html",
#         {"orders": orders}
#     )
# 
# 
# def update_order_status(request, order_id):
# 
#     order = get_object_or_404(Order, id=order_id)
# 
#     if request.method == "POST":
#         order.status = request.POST.get("status")
#         order.save()
# 
#     return redirect("order_list")
# 
# from cart.models import Cart
# 
# def place_order(request):
# 
#     cart_id = request.session.get("cart_id")
# 
#     if not cart_id:
#         return redirect("cart")
# 
#     try:
#         cart = Cart.objects.get(id=cart_id)
#     except Cart.DoesNotExist:
#         return redirect("cart")
# 
#     # Create new order
#     order = Order.objects.create()
# 
#     # Copy cart items to order items
#     for cart_item in cart.items.all():
# 
#         OrderItem.objects.create(
#             order=order,
#             menu_item=cart_item.menu_item,
#             quantity=cart_item.quantity
#         )
# 
#     # Delete all cart items
#     cart.items.all().delete()
# 
#     # Delete cart
#     cart.delete()
# 
#     # Remove cart from session
#     request.session.pop("cart_id", None)
# 
#     return redirect("order_list")