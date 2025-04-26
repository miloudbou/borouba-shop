import requests
from bs4 import BeautifulSoup
import csv

def fetch_best_selling_products():
    # الرابط الأساسي للمنتجات الأكثر مبيعًا في AliExpress
    url = "https://www.aliexpress.com/category/100003109/best-sellers.html"
    
    # إرسال طلب GET إلى الموقع
    response = requests.get(url)
    
    # التأكد من أن الاستجابة كانت ناجحة
    if response.status_code != 200:
        print("❌ حدث خطأ في تحميل الصفحة.")
        return
    
    # تحليل HTML باستخدام BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # العثور على جميع المنتجات
    products = soup.find_all('a', class_='item-title')

    if not products:
        print("❌ لم يتم العثور على أي منتجات.")
        return

    # فتح ملف CSV لتخزين البيانات
    with open("aliexpress_products.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Title", "Product Link"])  # كتابة العناوين في أول السطر

        # استخراج العناوين والروابط
        for product in products:
            title = product.get_text(strip=True)  # عنوان المنتج
            link = product.get('href')  # رابط المنتج
            writer.writerow([title, link])  # كتابة البيانات في الملف
            print(f"📦 {title} - 🔗 {link}")  # طباعة المنتج في الكونسول

    print("✅ تم حفظ المنتجات في ملف aliexpress_products.csv")

# تنفيذ الوظيفة
if __name__ == "__main__":
    fetch_best_selling_products()
