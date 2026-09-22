from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.reservation_list,
        name="reservation_list"
    ),

    path(
        "create/",
        views.create_reservation,
        name="create_reservation"
    ),

    path(
        "update-status/<int:reservation_id>/",
        views.update_reservation_status,
        name="update_reservation_status"
    ),

]