from django.shortcuts import render
import qrcode
import os
from django.conf import settings


def generate_qr(request):

    # url = "http://127.0.0.1:8000/menu/"
    url = request.build_absolute_uri('/menu/')

    qr = qrcode.make(url)

    qr_path = os.path.join(
        settings.MEDIA_ROOT,
        "menu_qr.png"
    )

    qr.save(qr_path)

    return render(
        request,
        "qrmenu/qr_page.html",
        {
            "qr_image": "/media/menu_qr.png"
        }
    )