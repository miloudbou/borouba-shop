from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# 🔹 نموذج التصنيف
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 🔹 نموذج المنتج (محدث لدعم AliExpress API)
class Product(models.Model):
    title = models.CharField(max_length=255)  # عنوان المنتج
    description = models.TextField(blank=True, null=True)  # وصف المنتج
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default=1)  # الفئة
    price = models.DecimalField(max_digits=10, decimal_places=2)  # السعر
    currency = models.CharField(max_length=10, default="دج")  # العملة الافتراضية
    image_url = models.URLField(blank=True, null=True)  # رابط الصورة
    affiliate_link = models.URLField(blank=True, null=True)  # رابط الإحالة من AliExpress
    aliexpress_product_id = models.CharField(max_length=50, blank=True, null=True)  # رقم المنتج في AliExpress
    created_at = models.DateTimeField(default=now)  # تاريخ الإضافة

    def get_price_display(self):
        """إرجاع السعر مع العملة"""
        return f"{self.price} {self.currency}"

    def __str__(self):
        return self.title

# 🔹 نموذج الشحن
class Shipping(models.Model):
    name = models.CharField(max_length=255)  # اسم طريقة الشحن
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # سعر الشحن
    estimated_time = models.CharField(max_length=255)  # الوقت المقدر للتسليم (مثل: 5-7 أيام)
    
    def __str__(self):
        return self.name

# 🔹 نموذج الدفع
class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)  # اسم طريقة الدفع (مثل: PayPal، نقدًا عند التسليم)
    
    def __str__(self):
        return self.name

# 🔹 نموذج الشراء كزائر
class GuestOrder(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    shipping_method = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True)  # ربط الشحن
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)  # ربط الدفع

    def __str__(self):
        return f"Order by {self.name} - {self.status}"

# 🔹 نموذج السلة
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"سلة {self.user.username if self.user else 'مجهول'}"

# 🔹 نموذج عنصر السلة
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} × {self.product.title}"

# 🔹 نموذج الطلب
class Order(models.Model):
    PAYMENT_METHODS = [
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cod')
    shipping_method = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True)  # ربط الشحن
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField()
    customer_phone = models.CharField(max_length=15)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def total_price(self):
        # إضافة تكلفة الشحن، وفي حال كان الشحن مجاني يتم إضافة صفر
        return sum(item.total_price() for item in self.items.all()) + (self.shipping_method.price if self.shipping_method else 0)

    def __str__(self):
        return f"Order {self.id} - {self.payment_method}"

# 🔹 نموذج عنصر الطلب
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} × {self.product.title} في الطلب {self.order.id}"