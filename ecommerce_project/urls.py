from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet  # type: ignore
from products import views
from products.views import test_500

# إعداد API
router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    # لوحة التحكم الخاصة بـ Django Admin
    path('admin/', admin.site.urls),

    # الصفحة الرئيسية للمنتجات
    path('', views.index, name='home'),


    # API المنتجات
    path('api/', include(router.urls)),

    # تضمين جميع مسارات تطبيق المنتجات
    path('products/', include('products.urls')),  # المسارات المتعلقة بالمنتجات
     path('test_500/', test_500),

]
