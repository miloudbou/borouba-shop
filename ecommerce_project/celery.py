import os
import django
from celery import Celery
from celery.schedules import crontab

# تعيين الإعدادات الافتراضية لـ Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

# إنشاء كائن Celery
app = Celery("ecommerce_project")

# تحميل إعدادات Celery من ملف settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# اكتشاف المهام تلقائيًا من التطبيقات المسجلة في المشروع
app.autodiscover_tasks()

# جدولة المهام إذا كنت تستخدم Celery Beat
app.conf.beat_schedule = {
    'fetch-products-daily': {
        'task': 'products.tasks.fetch_aliexpress_products',
        'schedule': crontab(hour=0, minute=0),  # تشغيل يوميًا عند منتصف الليل
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

