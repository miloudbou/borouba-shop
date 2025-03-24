import os
import subprocess

def run_script(script_name):
    """يشغل السكربتات بشكل متسلسل."""
    try:
        subprocess.check_call(['python', script_name])
        print(f"✅ تم تنفيذ {script_name} بنجاح!")
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل في تنفيذ {script_name}: {e}")

def main():
    fetch_products_script = os.path.join(os.getcwd(), 'products', 'fetch_products.py')
    clean_products_script = os.path.join(os.getcwd(), 'database', 'clean_products.py')
    database_script = os.path.join(os.getcwd(), 'database', 'database.py')

    # تشغيل سكربت جلب المنتجات من AliExpress
    print("🔄 بدء جلب المنتجات من AliExpress...")
    run_script(fetch_products_script)

    # تشغيل سكربت تنظيف البيانات
    print("🔄 بدء تنظيف البيانات...")
    run_script(clean_products_script)

    # تشغيل سكربت إدخال البيانات في قاعدة البيانات
    print("🔄 بدء إدخال المنتجات في قاعدة البيانات...")
    run_script(database_script)

if __name__ == "__main__":
    main()