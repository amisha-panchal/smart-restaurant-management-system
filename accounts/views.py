from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.conf import settings
import re
from django.contrib.auth.hashers import check_password

from django.core.mail import send_mail
from reservations.models import Reservation


from .models import CustomUser
from orders.models import Order,OrderItem
from django.db.models import Sum
from inventory.models import InventoryItem

#home
def home(request):
    return render(request, 'home.html')


#signup
def signup(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        if CustomUser.objects.filter(username=username).exists():
            return render(
                request,
                'signup.html',
                {'error': 'Username already exists'}
            )

        user= CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        login(request, user)
        return redirect('home')



    return render(request, 'signup.html')


#login
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect('home')

        return render(
            request,
            'login.html',
            {'error': 'Invalid Username or Password'}
        )

    return render(request, 'login.html')

#dashboard
from django.contrib.auth.decorators import login_required
# 
# @login_required
# def dashboard(request):
# 
#     role = request.user.role
# 
#     return render(
#         request,
#         'dashboard.html',
#         {'role': role}
#     )
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):

    # Customer cannot access dashboard
    if request.user.role == "customer":
        return redirect("home")

    total_orders = Order.objects.count()

    total_revenue = 0

    for item in OrderItem.objects.select_related(
        'menu_item'
    ):
        total_revenue += (
            item.menu_item.price * item.quantity
        )

    recent_orders = OrderItem.objects.select_related(
        'menu_item',
        'order'
    ).order_by(
        '-order__created_at'
    )[:5]

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    served_orders = Order.objects.filter(
        status='Served'
    ).count()

    preparing_orders = Order.objects.filter(
        status='Preparing'
    ).count()

    total_reservations = Reservation.objects.count()

    TOTAL_TABLES = 20

    occupied_tables = Reservation.objects.filter(
        status__in=[
            'Booked',
            'Seated'
        ]
    ).values(
        'table_number'
    ).distinct().count()

    available_tables = (
        TOTAL_TABLES - occupied_tables
    )

    upcoming_reservations = Reservation.objects.filter(
        status__in=[
            'Booked',
            'Seated'
        ]
    ).order_by(
        'reservation_time'
    )[:5]

    low_stock = InventoryItem.objects.filter(
        quantity__lte=10
    ).count()

    context = {

        'role': request.user.role,

        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,

        'pending_orders': pending_orders,
        'served_orders': served_orders,
        'preparing_orders': preparing_orders,

        'total_reservations': total_reservations,
        'available_tables': available_tables,
        'upcoming_reservations': upcoming_reservations,

        'low_stock': low_stock,
    }

    return render(
        request,
        'dashboard.html',
        context
    )
#logout
def logout_view(request):

    logout(request)

    return redirect('home')

#forgetpassword
import random
from django.core.mail import send_mail

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get('email')

        try:

            user = CustomUser.objects.get(email=email)

            otp = random.randint(100000, 999999)

            request.session['reset_email'] = email
            request.session['otp'] = str(otp)

            send_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            return redirect('verify_otp')

        except CustomUser.DoesNotExist:

            return render(
                request,
                'forgotpassword.html',
                {'error': 'Email not registered'}
            )

    return render(request, 'forgotpassword.html')

#reset Password
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
import re

from .models import CustomUser, PasswordResetHistory


def reset_password(request):

    if request.method == "POST":

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Password match validation
        if password1 != password2:
            return render(
                request,
                'reset_password.html',
                {'error': 'Passwords do not match'}
            )

        email = request.session.get('reset_email')

        if not email:
            return redirect('forgot_password')

        user = CustomUser.objects.get(email=email)

        # Cannot reuse old password
        if check_password(password1, user.password):
            return render(
                request,
                'reset_password.html',
                {
                    'error':
                    'New password cannot be the same as old password'
                }
            )

        # Minimum length
        if len(password1) < 8:
            return render(
                request,
                'reset_password.html',
                {
                    'error':
                    'Password must contain at least 8 characters'
                }
            )

        # Uppercase validation
        if not re.search(r'[A-Z]', password1):
            return render(
                request,
                'reset_password.html',
                {
                    'error':
                    'Password must contain at least one uppercase letter'
                }
            )

        # Lowercase validation
        if not re.search(r'[a-z]', password1):
            return render(
                request,
                'reset_password.html',
                {
                    'error':
                    'Password must contain at least one lowercase letter'
                }
            )

        # Number validation
        if not re.search(r'[0-9]', password1):
            return render(
                request,
                'reset_password.html',
                {
                    'error':
                    'Password must contain at least one number'
                }
            )

        # Special character validation
        if not re.search(r'[@$!%*?&#]', password1):
            return render(
                request,
                'reset_password.html',
                {
                    'error':
                    'Password must contain at least one special character'
                }
            )

        # Save Password
        user.set_password(password1)
        user.save()

        # Save Reset History
        PasswordResetHistory.objects.create(
            user=user,
            ip_address=request.META.get('REMOTE_ADDR'),
            success=True
        )

        # Success Email
        send_mail(
            'Password Changed Successfully',
            f'''
Hello {user.username},

Your password has been changed successfully.

If you did not perform this action,
please contact support immediately.

Smart Restaurant Management System
''',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        # Remove only reset session
        request.session.pop('reset_email', None)

        # Auto Login User
        login(request, user)

        # Success Message
        messages.success(
            request,
            '✅ Your password has been reset successfully.'
        )

        # Redirect Home
        return redirect('home')

    return render(
        request,
        'reset_password.html'
    )


# def reset_password(request):
# 
#     if request.method == "POST":
# 
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
# 
#         # Password match validation
#         if password1 != password2:
#             return render(
#                 request,
#                 'reset_password.html',
#                 {'error': 'Passwords do not match'}
#             )
# 
#         email = request.session.get('reset_email')
# 
#         if not email:
#             return redirect('forgot_password')
# 
#         user = CustomUser.objects.get(email=email)
# 
#         # Cannot reuse old password
#         if check_password(password1, user.password):
#             return render(
#                 request,
#                 'reset_password.html',
#                 {
#                     'error':
#                     'New password cannot be the same as old password'
#                 }
#             )
# 
#         # Minimum length
#         if len(password1) < 8:
#             return render(
#                 request,
#                 'reset_password.html',
#                 {
#                     'error':
#                     'Password must contain at least 8 characters'
#                 }
#             )
# 
#         # Uppercase validation
#         if not re.search(r'[A-Z]', password1):
#             return render(
#                 request,
#                 'reset_password.html',
#                 {
#                     'error':
#                     'Password must contain at least one uppercase letter'
#                 }
#             )
# 
#         # Lowercase validation
#         if not re.search(r'[a-z]', password1):
#             return render(
#                 request,
#                 'reset_password.html',
#                 {
#                     'error':
#                     'Password must contain at least one lowercase letter'
#                 }
#             )
# 
#         # Number validation
#         if not re.search(r'[0-9]', password1):
#             return render(
#                 request,
#                 'reset_password.html',
#                 {
#                     'error':
#                     'Password must contain at least one number'
#                 }
#             )
# 
#         # Special character validation
#         if not re.search(r'[@$!%*?&#]', password1):
#             return render(
#                 request,
#                 'reset_password.html',
#                 {
#                     'error':
#                     'Password must contain at least one special character'
#                 }
#             )
# 
#         # Save Password
#         user.set_password(password1)
#         user.save()
# 
#         # Save Reset History
#         PasswordResetHistory.objects.create(
#             user=user,
#             ip_address=request.META.get('REMOTE_ADDR'),
#             success=True
#         )
# 
#         # Success Email
#         send_mail(
#             'Password Changed Successfully',
#             f'''
# Hello {user.username},
# 
# Your password has been changed successfully.
# 
# If you did not perform this action,
# please contact support immediately.
# 
# Smart Restaurant Management System
# ''',
#             settings.EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False
#         )
# 
#         # Home Page Notification
#         messages.success(
#             request,
#             '✅ Your password has been reset successfully.'
#         )
# # 
# #         # Clear OTP Session
# #         request.session.flush()
# # 
# #         # Redirect Home
# #         return redirect('home')
#     request.session.pop('reset_email', None)
# 
#     login(request, user)
# 
#     return redirect('home')
# 
#     return render(
#         request,
#         'reset_password.html'
#     )

#verify_otp
def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get('otp')

        saved_otp = request.session.get('otp')

        if entered_otp == saved_otp:

            return redirect('reset_password')

        return render(
            request,
            'verify_otp.html',
            {'error': 'Invalid OTP'}
        )

    return render(request, 'verify_otp.html')