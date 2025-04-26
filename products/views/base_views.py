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
from products.forms import GuestOrderForm, ProductForm, OrderForm, EditProfileForm, AdminLoginForm, SiteSettingsForm, ContactForm 
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

# الصفحة الرئيسية
def index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})
# صفحة من نحن
def about_view(request):
    return render(request, 'products/about.html')
# صفحة  الشروط والأحكام
def terms(request):
    return render(request, 'products/terms.html')
# صفحة سياسة الخصوصية
def privacy(request):
    return render(request, 'products/privacy.html')

# عرض صفحة الاتصال
def contact(request):
    if request.method == 'POST':
        # إذا كان الطلب هو POST
        form = ContactForm(request.POST)
        if form.is_valid():
            # هنا يمكنك إرسال البيانات إلى البريد الإلكتروني أو حفظها في قاعدة البيانات
            # في الوقت الحالي نعرض رسالة بسيطة
            return HttpResponse("تم إرسال الرسالة بنجاح!")
    else:
        form = ContactForm()  # عرض نموذج فارغ عند الطلب GET

    return render(request, 'products/contact.html', {'form': form})
def submit_contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # يمكنك إرسال البيانات عبر البريد الإلكتروني أو حفظها في قاعدة البيانات
            return HttpResponse("تم إرسال الرسالة بنجاح!")
        else:
            return HttpResponse("هناك خطأ في النموذج")
    return redirect('contact')  # إعادة التوجيه إلى صفحة الاتصال إذا لم يكن الطلب POST


#(صفحة اختبار الأخطاء (للتطوير فقط
def test_500(request):
    return HttpResponseServerError("حدث خطأ داخلي في الخادم")
# صفحة الأسئلة الشائعة
def faq(request):
    faq_items = [
        {"question": "كيف يمكنني الشراء من المتجر؟", "answer": "اختر المنتج، أضفه إلى السلة، ثم تابع عملية الدفع."},
        {"question": "ما طرق الدفع المتوفرة؟", "answer": "نحن ندعم PayPal، Baridimob، بطاقة Visa، والدفع عند الاستلام."},
        {"question": "هل يمكنني تتبع طلبي؟", "answer": "نعم، إذا أنشأت حسابًا يمكنك تتبع الطلب من صفحة الطلبات."},
        {"question": "كم تستغرق مدة الشحن؟", "answer": "مدة الشحن تختلف حسب الولاية، وتتراوح من 2 إلى 5 أيام عمل."},
    ]
    return render(request, 'products/faq.html', {'faq_items': faq_items})
# صفحة سياسة الشحن
def shipping_policy(request):
    return render(request, 'products/shipping_policy.html')
# صفحة سياسة الإرجاع
def return_policy(request):
    return render(request, 'products/return_policy.html')
# صفحة تسجيل الدخول
