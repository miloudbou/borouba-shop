from django.contrib import admin
from .models import Product, Category
import re

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'image_url', 'created_at')

    def save_model(self, request, obj, form, change):
        # إزالة الفواصل ',' من السعر إن وجدت، واستبدالها بسعر صحيح
        obj.price = float(re.sub(r'[^\d.]', '', str(obj.price)))  
        obj.price = round(obj.price, 2)  # تقريب إلى منزلتين عشريتين
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)