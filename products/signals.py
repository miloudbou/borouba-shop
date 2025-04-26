from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


# إشارة بعد إضافة منتج جديد
@receiver(post_save, sender=Product)
def product_added(sender, instance, created, **kwargs):
    if created:
        print(f"تم إضافة منتج جديد: {instance.title}")

