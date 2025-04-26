from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from products.models import Product, Order, OrderItem, Category, Shipping, SiteSettings, Wishlist
from products.forms import GuestOrderForm, ProductForm, OrderForm, EditProfileForm, AdminLoginForm, SiteSettingsForm
from products.serializers import ProductSerializer
from rest_framework import viewsets
import logging
from django.http import HttpResponseServerError
from django.contrib.auth import logout
from django.utils.translation import get_language
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timedelta

# عرض صفحة تسجيل الدخول
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # بعد تسجيل الدخول يمكن توجيه المستخدم إلى الصفحة الرئيسية أو أي صفحة أخرى
        else:
            messages.error(request, "البريد الإلكتروني أو كلمة المرور غير صحيحة")
    
    return render(request, 'products/login.html')

# عرض صفحة التسجيل
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # حفظ المستخدم الجديد
            messages.success(request, "تم إنشاء الحساب بنجاح!")
            return redirect('login')  # بعد التسجيل يتم توجيه المستخدم إلى صفحة تسجيل الدخول
        else:
            messages.error(request, "حدث خطأ أثناء التسجيل.")
    else:
        form = UserCreationForm()

    return render(request, 'products/register.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # إعادة التوجيه إلى المسار home
# عرض صفحة الملف الشخصي
@login_required  # التأكد من أن المستخدم مسجل دخوله
def profile(request):
    return render(request, 'products/profile.html', {'user': request.user})
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # بعد الحفظ، إعادة توجيه إلى صفحة الملف الشخصي
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'products/edit_profile.html', {'form': form})