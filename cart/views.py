from django.shortcuts import render, redirect, get_object_or_404
from menu.models import MenuItem
from .models import Cart, CartItem
from django.shortcuts import redirect

def increase_quantity(request, item_id):

    cart_id = request.session.get("cart_id")

    if cart_id:
        cart = Cart.objects.get(id=cart_id)

        item = CartItem.objects.get(
            cart=cart,
            menu_item_id=item_id
        )

        item.quantity += 1
        item.save()

    return redirect("cart")


def decrease_quantity(request, item_id):
    

    cart_id = request.session.get("cart_id")

    if cart_id:
        cart = Cart.objects.get(id=cart_id)

        item = CartItem.objects.get(
            cart=cart,
            menu_item_id=item_id
        )

        if item.quantity > 1:
            item.quantity -= 1
            item.save()

    return redirect("cart")


def add_to_cart(request, item_id):

    item = get_object_or_404(MenuItem, id=item_id)

    cart_id = request.session.get("cart_id")

    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session["cart_id"] = cart.id

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=item
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("menu_list")


def cart_view(request):
    
  

    cart_id = request.session.get("cart_id")

    if not cart_id:
        return render(
            request,
            "cart/cart.html",
            {
                "cart": None
            }
        )

    cart = Cart.objects.prefetch_related(
        "items",
        "items__menu_item"
    ).get(id=cart_id)

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart
        }
    )


def remove_from_cart(request, item_id):

    cart_id = request.session.get("cart_id")

    if cart_id:
        cart = Cart.objects.get(id=cart_id)

        CartItem.objects.filter(
            cart=cart,
            menu_item_id=item_id
        ).delete()

    return redirect("cart")