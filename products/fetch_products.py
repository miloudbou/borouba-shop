import requests
import json
from django.conf import settings

# إعدادات API
ALIEXPRESS_API_URL = "https://api-sandbox.aliexpress.com"  # غيّر إلى API الحقيقي عند الموافقة
ALIEXPRESS_APP_KEY = settings.ALIEXPRESS_APP_KEY
ALIEXPRESS_ACCESS_TOKEN = settings.ALIEXPRESS_ACCESS_TOKEN

def fetch_products_from_aliexpress():
    """جلب المنتجات من AliExpress API"""
    url = f"{ALIEXPRESS_API_URL}/api"
    
    params = {
        "method": "aliexpress.product.list",
        "app_key": ALIEXPRESS_APP_KEY,
        "access_token": ALIEXPRESS_ACCESS_TOKEN,
        "page_size": 10,
        "page_no": 1
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])
        
        # حفظ المنتجات في ملف JSON
        with open("database/aliexpress_products.json", "w", encoding="utf-8") as file:
            json.dump(products, file, indent=4, ensure_ascii=False)

        print(f"✅ تم جلب {len(products)} منتجًا من AliExpress!")
        return products
    else:
        print(f"⚠️ فشل في جلب البيانات من AliExpress: {response.status_code}")
        return []

if __name__ == "__main__":
    fetch_products_from_aliexpress()


