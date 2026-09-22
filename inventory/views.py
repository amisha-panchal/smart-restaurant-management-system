from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import InventoryItem
from notifications.models import Notification


def inventory_list(request):

    if request.user.role != "admin":
        return redirect("home")

    items = InventoryItem.objects.all()

    return render(
        request,
        "inventory/inventory_list.html",
        {
            "items": items
        }
    )


def create_inventory_item(request):

    if request.user.role != "admin":
        return redirect("home")

    if request.method == "POST":

        item = InventoryItem.objects.create(
            name=request.POST.get("name"),
            quantity=request.POST.get("quantity"),
            unit=request.POST.get("unit"),
            minimum_stock=request.POST.get(
                "minimum_stock"
            )
        )

        if int(item.quantity) <= int(item.minimum_stock):

            Notification.objects.create(
                title="📦 Low Stock Alert",
                message=f"{item.name} stock is below minimum level"
            )

        return redirect(
            "inventory_list"
        )

    return render(
        request,
        "inventory/create_inventory.html"
    )


def edit_inventory_item(request, item_id):

    if request.user.role != "admin":
        return redirect("home")

    item = get_object_or_404(
        InventoryItem,
        id=item_id
    )

    if request.method == "POST":

        item.name = request.POST.get("name")

        item.quantity = request.POST.get("quantity")

        item.unit = request.POST.get("unit")

        item.minimum_stock = request.POST.get(
            "minimum_stock"
        )

        item.save()

        if int(item.quantity) <= int(item.minimum_stock):

            Notification.objects.create(
                title="📦 Low Stock Alert",
                message=f"{item.name} stock is below minimum level"
            )

        return redirect(
            "inventory_list"
        )

    return render(
        request,
        "inventory/edit_inventory.html",
        {
            "item": item
        }
    )


def delete_inventory_item(request, item_id):

    if request.user.role != "admin":
        return redirect("home")

    item = get_object_or_404(
        InventoryItem,
        id=item_id
    )

    Notification.objects.create(
        title="🗑 Inventory Deleted",
        message=f"{item.name} has been removed from inventory"
    )

    item.delete()

    return redirect(
        "inventory_list"
    )