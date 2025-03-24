from django.contrib import admin
from .models import Product, Category

# تخصيص واجهة الإدارة لعرض الحقول المناسبة
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'image_url', 'created_at')  # تعديل الحقول هنا لتطابق الحقول الفعلية في نموذج Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)



