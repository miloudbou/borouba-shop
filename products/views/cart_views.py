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
  


# عرض سلة التسوق للمستخدم المسجل
@login_required(login_url="login")  # يجبر المستخدم على تسجيل الدخول قبل الوصول إلى السلة
def view_cart(request):
    try:
        order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
        cart_items = order.items.all()
        total_price = sum(item.total_price() for item in cart_items)
    except Exception as e:
        logger.error(f"خطأ في عرض السلة: {e}")
        messages.error(request, "❌ حدث خطأ أثناء عرض السلة.")
        return redirect("index")

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'language': get_language(),
    })

# إضافة منتج إلى السلة للمستخدم المسجل
@login_required
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
        order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)
        if not item_created:
            order_item.quantity += 1
        order_item.save()

        logger.info(f"تم إضافة المنتج {product.title} إلى السلة.")
        return JsonResponse({"success": True, "message": "تمت الإضافة بنجاح!"})
    except Exception as e:
        logger.error(f"خطأ في إضافة المنتج إلى السلة: {e}")
        return JsonResponse({"success": False, "message": "حدث خطأ أثناء إضافة المنتج."})

# تحديث كمية المنتج في السلة
@login_required
def update_cart(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        order = Order.objects.get(user=request.user, is_paid=False)
        order_item = get_object_or_404(OrderItem, order=order, product_id=product_id)
        order_item.quantity = quantity
        order_item.save()
    return redirect("view_cart")

# حذف منتج من السلة
@login_required
def remove_from_cart(request, product_id):
    order = Order.objects.get(user=request.user, is_paid=False)
    order.items.filter(product_id=product_id).delete()
    return redirect("view_cart")