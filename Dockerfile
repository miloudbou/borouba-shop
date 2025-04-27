# استخدام صورة Python 3.10 slim
FROM python:3.10-slim

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ الملفات المحلية إلى الحاوية
COPY . /app/

# تحديث pip إلى الإصدار الأخير
RUN pip install --upgrade pip

# تثبيت الأدوات الأساسية لبناء الحزم
RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev

# تثبيت الحزم المطلوبة من ملف requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# إعداد متغير البيئة للإشارة إلى إعدادات الإنتاج
ENV PYTHONUNBUFFERED 1

# فتح المنفذ الذي سيعمل عليه التطبيق
EXPOSE 8000

# تشغيل الخادم المحلي عند بدء الحاوية
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
