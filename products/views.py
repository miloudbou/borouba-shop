from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from .models import Product, Order, OrderItem, Category, Shipping
from .forms import GuestOrderForm
from .serializers import ProductSerializer
from rest_framework import viewsets
import logging
from django.http import HttpResponseServerError
from django.contrib.auth import logout
from django.utils.translation import get_language


# إعداد السجل (Logging)
logger = logging.getLogger(__name__)

# إعداد PayPal
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # "sandbox" أو "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})

def create_payment(request):
    """إنشاء معاملة دفع جديدة في PayPal"""
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/paypal/execute-payment/",
            "cancel_url": "http://127.0.0.1:8000/cart/"
        },
        "transactions": [{
            "amount": {"total": "10.00", "currency": "USD"},
            "description": "شراء منتج من بوروبة شوب"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return JsonResponse({"approval_url": link.href})
    else:
        return JsonResponse({"error": payment.error}, status=500)

def execute_payment(request):
    """تنفيذ الدفع بعد موافقة المستخدم"""
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return JsonResponse({"status": "success", "message": "تم الدفع بنجاح!"})
    else:
        return JsonResponse({"status": "error", "message": payment.error})

# عرض API للمنتجات
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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

# عرض صفحة الدفع
def payment_page(request):
    shipping_methods = Shipping.objects.all()  # جلب جميع طرق الشحن المتاحة
    payment_methods = Order.PAYMENT_METHODS  # طرق الدفع المتاحة (PayPal, COD)
    
    return render(request, 'products/payment.html', {
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods
    })

# تنفيذ الدفع عبر PayPal
def create_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', '100')
        currency = request.POST.get('currency', settings.DEFAULT_CURRENCY)

        if currency == "DZD":
            try:
                amount = float(amount) * settings.EXCHANGE_RATE_DZD_TO_USD
                amount = round(amount, 2)
            except ValueError:
                logger.error("قيمة المبلغ غير صحيحة.")
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
                logger.error("فشل إنشاء الدفع: %s", payment.error)
                return JsonResponse({'error': 'فشل في إنشاء الدفع', 'details': payment.error}, status=400)
        except Exception as e:
            logger.error(f"خطأ أثناء إنشاء الدفع: {e}")
            return JsonResponse({'error': 'حدث خطأ أثناء إنشاء الدفع.'}, status=500)

    return render(request, 'products/payment.html')

# تنفيذ الدفع بعد موافقة المستخدم
def execute_payment(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    try:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            messages.success(request, "✅ تم الدفع بنجاح!")
            return redirect('payment_success')
        else:
            logger.error(f"فشل الدفع: {payment.error}")
            messages.error(request, "❌ فشل الدفع!")
            return redirect('payment_failed')

    except Exception as e:
        logger.error(f"خطأ أثناء تنفيذ الدفع: {e}")
        messages.error(request, "حدث خطأ أثناء معالجة الدفع!")
        return redirect('payment_failed')

def payment_success(request):
    return render(request, "products/payment_success.html")

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

# عرض التصنيفات
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

# عرض المنتجات ضمن تصنيف معين
def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_products.html', {'category': category, 'products': products})

# الصفحة الرئيسية
def index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})

# عرض تفاصيل المنتج
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/single.html', {'product': product})

# عرض صفحة الاتصال
def contact(request):
    return render(request, 'products/contact.html')

# صفحة فشل الدفع
def payment_failed(request):
    return render(request, "products/payment_failed.html")

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

# عرض البحث عن المنتجات
def product_search(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(title__icontains=query) if query else Product.objects.all()
    return render(request, 'products/search.html', {'products': products})

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

def test_500(request):
    # رفع خطأ 500 يدويا
    return HttpResponseServerError("حدث خطأ داخلي في الخادم")
def offers(request):
    offers = Product.objects.filter(is_offer=True)
    return render(request, "products/offers.html", {"offers": offers})

def logout_view(request):
    logout(request)
    return redirect('home')