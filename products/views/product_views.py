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

# عرض قائمة المنتجات مع البحث والتصفية
def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    if search_query:
        products = products.filter(title__icontains=search_query)
    
    if category_id.isdigit():
        products = products.filter(category__id=int(category_id))

    return render(request, 'products/product_list.html', {
        'products': products,
        'search': search_query,
        'category': category_id
    })
# عرض تفاصيل المنتج
def product_detail(request, product_id):
    # نحاول جلب المنتج باستخدام ID المنتج، وإذا لم نتمكن من ذلك نقوم بإرجاع صفحة 404
    product = get_object_or_404(Product, id=product_id)

    # إنشاء القاموس الذي يحتوي على البيانات التي سيتم تمريرها إلى القالب
    context = {
        'product': product,  # المنتج الذي تم جلبه
        'stars_range': range(1, 6),  # النطاق لعدد النجوم (من 1 إلى 5)
    }

    # عرض القالب 'single.html' مع تمير البيانات (context)
    return render(request, 'products/single.html', context)

# عرض صفحة البحث عن المنتجات

def product_search(request):
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'newest')
    page_number = request.GET.get('page', 1)
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'sold':
        products = products.order_by('-sold_count')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'query': query,
        'sort_by': sort_by,
        'category_id': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'categories': categories,
        'products': page_obj.object_list,
        'results_count': products.count(),
        'page_obj': page_obj
    }

    return render(request, 'products/search.html', context)

def search_suggestions(request):
    query = request.GET.get('term', '').strip()
    suggestions = []

    if query:
        suggestions = Product.objects.filter(
            Q(title__icontains=query)
        ).values_list('title', flat=True).distinct()[:10]

    return JsonResponse(list(suggestions), safe=False)


def new_arrivals(request):
    from datetime import datetime, timedelta
    new_products = Product.objects.filter(
        created_at__gte=datetime.now()-timedelta(days=30)
    ).order_by('-created_at')
    
    context = {
        'products': new_products,
        'title': 'وصل حديثاً'
    }
    return render(request, 'products/product_list.html', context)

def offers(request):
    offers = Product.objects.filter(is_offer=True)
    return render(request, "products/offers.html", {"offers": offers})

def flash_sale(request):
    now = timezone.now()
    products = Product.objects.filter(is_flash_sale=True, flash_sale_end__gt=now)
    return render(request, 'products/flash_sale.html', {'products': products, 'now': now})

def top_selling(request):
    products = Product.objects.order_by('-sold_count')[:20]  # عدّل حسب الترتيب الذي تستخدمه
    return render(request, 'products/top_selling.html', {'products': products})

def blog_list(request):
    return render(request, 'products/blog_list.html')

# عرض API للمنتجات
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer