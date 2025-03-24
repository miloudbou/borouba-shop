from celery import shared_task
from celery import shared_task
import requests
from django.conf import settings
from .models import Product

@shared_task
def fetch_aliexpress_products():
    url = f"{settings.ALIEXPRESS_API_URL}/api"
    
    params = {
        "method": "aliexpress.product.list",
        "app_key": settings.ALIEXPRESS_APP_KEY,
        "access_token": settings.ALIEXPRESS_ACCESS_TOKEN,
        "page_size": 10,
        "page_no": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    for item in data.get("products", []):
        Product.objects.update_or_create(
            ali_express_id=item["product_id"],
            defaults={
                "name": item["title"],
                "price": item["price"],
                "image_url": item["image_url"],
            }
        )
    
    return "تم استيراد المنتجات بنجاح!"



