from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.reports_dashboard,
        name='reports'
    ),

    path(
        'export-pdf/',
        views.export_pdf,
        name='export_pdf'
    ),
    path(
        'export-excel/',
        views.export_excel,
        name='export_excel'
    ),

]