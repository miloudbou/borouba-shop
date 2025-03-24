# استخدام صورة Python الرسمية من Docker Hub
FROM python:3.8-slim

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ الملفات المحلية إلى الحاوية
COPY . /app/

# تثبيت الحزم المطلوبة من ملف requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# إعداد متغير البيئة للإشارة إلى إعدادات الإنتاج
ENV PYTHONUNBUFFERED 1

# فتح المنفذ الذي سيعمل عليه التطبيق
EXPOSE 8000

# تشغيل الخادم المحلي عند بدء الحاوية
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]