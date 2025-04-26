from django.contrib import admin
from .models import Product, Category
import re
from .models import SiteSettings

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_active', 'sold_count', 'rating', 'reviews_count', 'created_at', 'shipping_info')  # عرض الحقول الجديدة في قائمة المنتجات
    list_filter = ('is_active', 'category', 'is_offer', 'is_flash_sale')  # فلاتر المنتجات
    search_fields = ('title', 'description')  # حقول البحث
    list_editable = ('is_active',)  # تحرير حالة النشاط مباشرة
    ordering = ('-created_at',)  # ترتيب المنتجات حسب تاريخ الإضافة
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'price', 'original_price', 'currency', 'image_url', 'affiliate_link', 'is_offer', 'is_flash_sale', 'sold_count', 'is_active', 'rating', 'reviews_count', 'shipping_info')
        }),
        ('خصائص العرض', {
            'fields': ('flash_sale_end',)
        }),
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(SiteSettings)