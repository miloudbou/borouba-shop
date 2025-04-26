from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

# استيراد views حسب التقسيم الجديد
from .views.product_views import ProductViewSet, product_list, product_detail, product_search, search_suggestions, new_arrivals, offers, flash_sale, top_selling, blog_list
from .views.cart_views import view_cart, add_to_cart, update_cart, remove_from_cart
from .views.order_views import create_order, order_history
from .views.payment_views import (
    create_or_execute_payment, choose_payment_method, process_payment_method,
    payment_success, payment_failed, baridimob_payment, visa_payment,
    cash_on_delivery, process_visa_payment, process_baridimob_payment,
    payment_page
)
from .views.category_views import category_list, category_products
from .views.auth_views import login_view, register_view, logout_view, profile, edit_profile
from .views.base_views import index, about_view, terms, privacy, contact, faq, shipping_policy, return_policy, test_500, submit_contact_form
from .views.wishlist_views import wishlist, add_to_wishlist, remove_from_wishlist
from .views.admin_views import (
    admin_login, admin_dashboard, manage_products, manage_orders,
    manage_users, site_settings, edit_product, delete_product,
    edit_user, delete_user, change_user_password
)

# إعداد API
router = DefaultRouter()
router.register(r'api/products', ProductViewSet)

urlpatterns = [
    # 🏠 الرئيسية
    path('', index, name='home'),

    # 🛒 المنتجات
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),

    # 🛍️ السلة والشراء
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    # 💳 الدفع
    path('payment/', payment_page, name='payment_page'),
    path('payment/choose/', choose_payment_method, name='choose_payment'),
    path('payment/process/', process_payment_method, name='process_payment_method'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failed/', payment_failed, name='payment_failed'),

    # طرق الدفع الفردية
    path('payment/baridimob/', baridimob_payment, name='baridimob_payment'),
    path('payment/visa/', visa_payment, name='visa_payment'),
    path('payment/paypal/', create_or_execute_payment, name='paypal_payment'),
    path('payment/execute/', create_or_execute_payment, name='paypal_execute'),
    path('payment/cancel/', payment_failed, name='paypal_cancel'),
    path('payment/cash/', cash_on_delivery, name='cash_on_delivery'),

    # معالجة طرق الدفع
    path('payment/visa/process/', process_visa_payment, name='process_visa_payment'),
    path('payment/baridimob/process/', process_baridimob_payment, name='process_baridimob_payment'),

    # 🧾 التصنيفات والعروض
    path('categories/', category_list, name='category_list'),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('offers/', offers, name='offers'),
    path('flash-sale/', flash_sale, name='flash_sale'),
    path('top-selling/', top_selling, name='top_selling'),
    path('blog/', blog_list, name='blog_list'),

    # 📞 الاتصال
    path('contact/', contact, name='contact'),
    path('submit_contact/', submit_contact_form, name='submit_contact_form'),
    
    # ✅ الطلبات
    path('order/create/', create_order, name='create_order'),
    path('orders/history/', order_history, name='order_history'),

    # 🔎 البحث
    path('search/', product_search, name='product_search'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),

    # 👤 تسجيل الدخول والتسجيل
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    # معلومات إضافية
    path('about/', about_view, name='about'),
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('new-arrivals/', new_arrivals, name='new_arrivals'),
    path('faq/', faq, name='faq'),
    path('shipping-policy/', shipping_policy, name='shipping_policy'),
    path('return-policy/', return_policy, name='return_policy'),

    # ⚙️ لوحة تحكم المسؤول
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('manage-products/', manage_products, name='manage_products'),
    path('manage-orders/', manage_orders, name='manage_orders'),
    path('manage-users/', manage_users, name='manage_users'),
    path('admin/settings/', site_settings, name='site_settings'),
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('change-password/<int:user_id>/', change_user_password, name='change_user_password'),

    # 🧪 اختبار الأخطاء
    path("test-500/", test_500, name="test_500"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 🔗 روابط الـ API
urlpatterns += router.urls








