from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.bill_list,
        name="bill_list"
    ),

    path(
        "generate/<int:order_id>/",
        views.generate_bill,
        name="generate_bill"
    ),
    path(
    "invoice/<int:bill_id>/",
    views.invoice_detail,
    name="invoice_detail"
),
 path(
        "invoice/pdf/<int:bill_id>/",
        views.download_invoice_pdf,
        name="download_invoice_pdf"
    ),
]