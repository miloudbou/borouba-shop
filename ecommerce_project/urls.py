from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, test_500  
from products import views 
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
    path('products/', include('products.urls')),

    # اختبار خطأ 500
    path('test_500/', test_500),
   
 ]

# إعداد الملفات الثابتة في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
