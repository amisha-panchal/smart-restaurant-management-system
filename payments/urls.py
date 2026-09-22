from django.urls import path
from . import views

urlpatterns = [

    path(
        'checkout/<int:order_id>/',
        views.checkout,
        name='checkout'
    ),

    path(
        'history/',
        views.payment_history,
        name='payment_history'
    ),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
]