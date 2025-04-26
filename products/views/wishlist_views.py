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

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
        'title': 'قائمة الرغبات'
    }
    return render(request, 'products/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        wishlist_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')

def faq(request):
    faq_items = [
        {"question": "كيف يمكنني الشراء من المتجر؟", "answer": "اختر المنتج، أضفه إلى السلة، ثم تابع عملية الدفع."},
        {"question": "ما طرق الدفع المتوفرة؟", "answer": "نحن ندعم PayPal، Baridimob، بطاقة Visa، والدفع عند الاستلام."},
        {"question": "هل يمكنني تتبع طلبي؟", "answer": "نعم، إذا أنشأت حسابًا يمكنك تتبع الطلب من صفحة الطلبات."},
        {"question": "كم تستغرق مدة الشحن؟", "answer": "مدة الشحن تختلف حسب الولاية، وتتراوح من 2 إلى 5 أيام عمل."},
    ]
    return render(request, 'products/faq.html', {'faq_items': faq_items})

def shipping_policy(request):
    return render(request, 'products/shipping_policy.html')

def return_policy(request):
    """
    عرض سياسة الإرجاع للمستخدمين بشكل احترافي
    """
    return render(request, 'products/return_policy.html')

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:  # التحقق من أن المستخدم هو مسؤول
                login(request, user)
                return redirect('admin_dashboard')  # يمكنك توجيههم إلى لوحة التحكم الخاصة بك
            else:
                messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة أو ليس لديك صلاحيات المسؤول.')
    else:
        form = AdminLoginForm()

    return render(request, 'products/admin_login.html', {'form': form})

def create_admin_groups():
    if not Group.objects.filter(name="Admin").exists():
        group = Group.objects.create(name="Admin")
        # إضافة صلاحيات معينة للمجموعة إذا لزم الأمر
@login_required
def admin_dashboard(request):
    is_admin_group = request.user.groups.filter(name='Admin').exists()
    return render(request, 'products/admin_dashboard.html', {
        'is_admin_group': is_admin_group
    })

def assign_permissions(user, role):
    if role == 'superadmin':
        group = Group.objects.get(name='SuperAdmin')
    elif role == 'admin':
        group = Group.objects.get(name='Admin')
    else:
        return
    
    user.groups.add(group)
    user.save()

def manage_products(request):
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.all()
    return render(request, 'products/manage_products.html', {'products': products, 'search_query': search_query})
    
    # تحقق من الأذونات
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')  # العودة للوحة التحكم إذا لم يكن لديه صلاحيات

    products = Product.objects.all()  # استرجاع جميع المنتجات
    return render(request, 'products/manage_products.html', {'products': products}) 

def manage_orders(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    # تحقق من الأذونات
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')

    orders = Order.objects.all()  # استرجاع جميع الطلبات
    return render(request, 'products/manage_orders.html', {'orders': orders})

def manage_users(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    if not request.user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')
    
    users = User.objects.all()  # استرجاع جميع المستخدمين
    return render(request, 'products/manage_users.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def site_settings(request):
    settings = SiteSettings.objects.first()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "تم حفظ الإعدادات بنجاح.")
    else:
        form = SiteSettingsForm(instance=settings)

    return render(request, 'products/site_settings.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product,
    })

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('manage_products')

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    groups = Group.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        group_id = request.POST.get('group')
        is_active = request.POST.get('is_active') == 'on'

        user.username = username
        user.email = email
        user.is_active = is_active
        user.save()

        if group_id:
            group = get_object_or_404(Group, pk=group_id)
            user.groups.clear()
            user.groups.add(group)

        return redirect('manage_users')

    return render(request, 'products/edit_user.html', {'user': user, 'groups': groups})




def change_user_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect('manage_users')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'products/change_password.html', {'form': form, 'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # أولًا نحذف الملف الشخصي إذا كان موجود
    try:
        user.profile.delete()
    except Profile.DoesNotExist:
        pass  # إذا لم يكن له ملف شخصي نتجاهل الخطأ

    # ثم نحذف المستخدم
    user.delete()

    return redirect('manage_users')  # أو أي صفحة مناسبة