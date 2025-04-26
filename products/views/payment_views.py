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

def create_or_execute_payment(request):
    """إنشاء أو تنفيذ الدفع عبر PayPal"""

    if request.method == 'POST':
        return handle_payment_creation(request)
    elif request.method == 'GET':
        return handle_payment_execution(request)
    # عرض نموذج الدفع في حال الطلب غير POST أو GET
    return render(request, 'products/payments/paypal_payment.html')

def handle_payment_creation(request):
    """إنشاء معاملة جديدة عبر PayPal"""
    amount = request.POST.get('amount', '100')
    currency = request.POST.get('currency', settings.DEFAULT_CURRENCY)

    try:
        amount = float(amount)
        if currency == "DZD":
            amount *= settings.EXCHANGE_RATE_DZD_TO_USD
        amount = round(amount, 2)
    except ValueError:
        logger.error("❌ Invalid amount value.")
        return JsonResponse({'error': 'قيمة المبلغ غير صحيحة'}, status=400)

    try:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment/execute/'),
                "cancel_url": request.build_absolute_uri('/payment/cancel/')
            },
            "transactions": [{
                "amount": {"total": str(amount), "currency": "USD"},
                "description": "الدفع مقابل المنتجات"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            logger.error(f"❌ Failed to create payment: {payment.error}")
            return JsonResponse({'error': 'فشل في إنشاء الدفع', 'details': payment.error}, status=400)

    except Exception as e:
        logger.exception("⚠️ Exception during payment creation.")
        return JsonResponse({'error': 'حدث خطأ أثناء إنشاء الدفع.'}, status=500)
def handle_payment_execution(request):
    """تنفيذ الدفع بعد موافقة المستخدم"""
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    if not payment_id or not payer_id:
        messages.error(request, "❌ معلومات الدفع غير كاملة.")
        return redirect('payment_failed')

    try:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            messages.success(request, "✅ تم الدفع بنجاح!")
            return redirect('payment_success')
        else:
            logger.error(f"❌ Payment execution failed: {payment.error}")
            messages.error(request, "❌ فشل الدفع!")
            return redirect('payment_failed')

    except Exception as e:
        logger.exception("⚠️ Exception during payment execution.")
        messages.error(request, "حدث خطأ أثناء معالجة الدفع!")
        return redirect('payment_failed')
# واجهة اختيار وسيلة الدفع
def choose_payment_method(request):
    return render(request, 'products/choose_payment_method.html')
# معالجة وسيلة الدفع المختارة
def process_payment_method(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        print(f"🔍 طريقة الدفع المختارة: {method}")

        if method == 'paypal':
            return redirect('paypal_payment')
        elif method == 'visa':
            return redirect('visa_payment')
        elif method == 'baridimob':
            return redirect('baridimob_payment')
        elif method == 'cash':
            return redirect('cash_on_delivery')  # إذا كنت عامل صفحة لها
        else:
            return redirect('payment_failed')
    return redirect('choose_payment')
# صفحات الدفع الأخرى
def cash_on_delivery(request):
    return render(request, 'products/cash_on_delivery.html')
def baridimob_payment(request):
    return render(request, 'products/baridimob_payment.html')
def visa_payment(request):
    return render(request, 'products/visa_payment.html')
def process_visa_payment(request):
    """معالجة الدفع عبر Visa"""
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        # تنفيذ منطق الدفع عبر Visa هنا
        # يمكنك محاكاة معاملة أو الاتصال بخدمة خارجية لمعالجة الدفع
        if card_number and expiry_date and cvv:
            messages.success(request, "✅ تم الدفع بنجاح عبر Visa!")
            return redirect('payment_success')
        else:
            messages.error(request, "❌ فشل الدفع! يرجى المحاولة مرة أخرى.")
            return redirect('payment_failed')
    return redirect('choose_payment')
def process_baridimob_payment(request):
    """معالجة الدفع عبر Baridimob"""
    if request.method == 'POST':
        baridimob_number = request.POST.get('baridimob_number')  # رقم حساب Baridimob
        amount = request.POST.get('amount')  # المبلغ الذي سيتم دفعه

        # تحقق من صحة البيانات
        if not baridimob_number or not amount:
            messages.error(request, "❌ يرجى ملء جميع البيانات المطلوبة.")
            return redirect('baridimob_payment')  # العودة إلى صفحة الدفع عبر Baridimob

        try:
            # تنفيذ منطق الدفع عبر Baridimob (محاكاة أو ربط بخدمة خارجية)
            # في حال كان لديك API معتمد، يمكنك إجراء الاتصال هنا
            # مثال محاكاة نجاح الدفع:
            if float(amount) > 0:  # إذا كانت قيمة المبلغ صحيحة
                messages.success(request, "✅ تم الدفع بنجاح عبر Baridimob!")
                return redirect('payment_success')  # إعادة توجيه إلى صفحة النجاح
            else:
                messages.error(request, "❌ المبلغ غير صحيح. يرجى المحاولة مرة أخرى.")
                return redirect('baridimob_payment')  # العودة إلى صفحة الدفع عبر Baridimob
        except Exception as e:
            logger.error(f"خطأ أثناء معالجة الدفع عبر Baridimob: {e}")
            messages.error(request, "❌ حدث خطأ أثناء معالجة الدفع.")
            return redirect('payment_failed')  # العودة إلى صفحة الفشل

    # إذا لم يكن الطلب من نوع POST، نقوم بإعادة توجيه المستخدم إلى صفحة الدفع عبر Baridimob
    return redirect('baridimob_payment')

def payment_view(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        
        if method == 'paypal':
            return redirect('paypal_payment')
        elif method == 'visa':
            return redirect('visa_payment')
        elif method == 'baridimob':
            return redirect('baridimob_payment')
        elif method == 'cash':
            return redirect('cash_on_delivery')
        else:
            return redirect('payment')  # fallback
    return render(request, 'products/choose_payment_method.html')
# عرض صفحة اختيار وسيلة الدفع
def payment_page(request):
    shipping_methods = Shipping.objects.all()  # جلب جميع طرق الشحن المتاحة
    return render(request, 'products/choose_payment_method.html', {
        'shipping_methods': shipping_methods,
    })
def payment_success(request):
    return render(request, "products/payment_success.html")
# صفحة فشل الدفع
def payment_failed(request):
    return render(request, "products/payment_failed.html")