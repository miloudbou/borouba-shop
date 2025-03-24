from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet  # تأكد من استيراد ProductViewSet
from . import views
from .views import test_500

# إعداد API
router = DefaultRouter()
router.register(r'api/products', ProductViewSet)  # مسار API للمنتجات

urlpatterns = [
    # مسارات عرض المنتجات
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    
    # مسارات السلة
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # مسارات الدفع
    path('payment/', views.payment_page, name='payment_page'),
    path('payment/create/', views.create_payment, name='create_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    
    # مسارات التصنيفات
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    
    # مسار الاتصال
    path('contact/', views.contact, name='contact'),
    
    # مسار إنشاء الطلب
    path('order/create/', views.create_order, name='create_order'),

    path('search/', views.product_search, name='search'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path("test-500/", test_500, name="test_500"),
]

# إضافة روابط API من الروتر
urlpatterns += router.urls










