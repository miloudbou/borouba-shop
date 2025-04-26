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

# إنشاء طلب جديد للمستخدم المسجل
@login_required
def create_order(request):
    if request.method == "POST":
        shipping_method_id = request.POST.get('shipping_method')
        payment_method = request.POST.get('payment_method')
                # جلب طريقة الشحن من قاعدة البيانات
        shipping_method = get_object_or_404(Shipping, id=shipping_method_id)
        
        try:
            order = Order.objects.get(user=request.user, is_paid=False)
            order.shipping_method = shipping_method
            order.payment_method = payment_method
            order.is_paid = True  # عند إتمام الطلب، يصبح مدفوعًا
            order.save()

            messages.success(request, "✅ تم إتمام الطلب بنجاح!")
            return redirect("order_success")
        except Order.DoesNotExist:
            messages.error(request, "❌ لم يتم العثور على الطلب.")
            return redirect("view_cart")
    
    return redirect("view_cart")
# صفحة نجاح الطلب
def order_success(request):
    return render(request, "products/order_success.html")
# إنشاء طلب كزائر
def create_guest_order(request):
    if request.method == 'POST':
        form = GuestOrderForm(request.POST)
        if form.is_valid():
            guest_order = form.save()  # حفظ الطلب كزائر
            shipping_method_id = request.POST.get('shipping_method')
            payment_method = request.POST.get('payment_method')

            # جلب طريقة الشحن من قاعدة البيانات
            shipping_method = get_object_or_404(Shipping, id=shipping_method_id)
            guest_order.shipping_method = shipping_method
            guest_order.payment_method = payment_method
            guest_order.save()  # حفظ التعديلات على الطلب كزائر

            messages.success(request, "✅ تم إنشاء طلبك كزائر بنجاح!")
            return redirect('payment_page')
        else:
            messages.error(request, "❌ حدث خطأ أثناء إنشاء الطلب كزائر.")
    else:
        form = GuestOrderForm()

    shipping_methods = Shipping.objects.all()
    payment_methods = Order.PAYMENT_METHODS
    return render(request, 'products/create_guest_order.html', {
        'form': form,
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods
    })

@login_required  # المستخدم لازم يكون مسجّل دخوله
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # أو حسب اسم الحقل
    return render(request, 'products/order_history.html', {'orders': orders})    


@login_required
def checkout(request):
    # احصل على السلة الخاصة بالمستخدم
    cart_items = request.session.get('cart', {})

    # إذا كانت السلة فارغة، يمكنك إعادة التوجيه إلى صفحة المنتجات
    if not cart_items:
        messages.warning(request, "سلتك فارغة. أضف منتجات قبل المتابعة.")
        return redirect('product_list')

    # استرجاع بيانات المستخدم مثل العنوان
    user = request.user
    order_form = OrderForm(instance=user.profile)  # إذا كان لديك نموذج عنوان خاص بك

    # حساب المجموع الكلي للسلة
    total_price = 0
    for item_id, quantity in cart_items.items():
        product = Product.objects.get(id=item_id)
        total_price += product.price * quantity

    # عندما يرسل المستخدم النموذج
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # إنشاء طلب جديد
            order = form.save(commit=False)
            order.user = user
            order.total_price = total_price
            order.save()

            # إضافة العناصر إلى الطلب
            for item_id, quantity in cart_items.items():
                product = Product.objects.get(id=item_id)
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

            # مسح السلة بعد إتمام الطلب
            request.session['cart'] = {}

            # إرسال بريد تأكيد للزبون
            send_mail(
                'تأكيد طلبك في بوروبة شوب',
                f'شكرًا لك! تم تقديم طلبك بنجاح. رقم الطلب: {order.id}. سيتم التواصل معك قريباً.',
                'info@borobashop.com',
                [user.email],
                fail_silently=False,
            )

            # إعادة التوجيه إلى صفحة النجاح
            messages.success(request, "تمت إضافة طلبك بنجاح!")
            return redirect('products:order_success', order_id=order.id)

    return render(request, 'products/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'order_form': order_form
    })