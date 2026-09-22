from django.urls import path
from . import views

urlpatterns = [
    path(
        'create/<int:item_id>/',
        views.create_order,
        name='create_order'
    ),
    path(
        '',
        views.order_list,
        name='order_list'
    ),
    path(
    'update-status/<int:order_id>/',
    views.update_order_status,
    name='update_order_status'
),

path(
    'place-order/',
    views.place_order,
    name='place_order'
),

    path(
        'history/',
        views.order_history,
        name='order_history'
    ),
    path(
    'manage/',
    views.manage_orders,
    name='manage_orders'
),
]