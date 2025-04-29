from pathlib import Path
import os
import mimetypes
import environ


# قراءة القيم من ملف .env
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# استخدام environ لقراءة DATABASE_URL
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://localhost:5432/mydb?sslmode=require'),
}
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
}
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(",")
# إعدادات AliExpress API
ALIEXPRESS_API_URL = "https://api-sandbox.aliexpress.com"
ALIEXPRESS_APP_KEY = "ضع_المفتاح_هنا"
ALIEXPRESS_SECRET = "ضع_السر_هنا"
ALIEXPRESS_ACCESS_TOKEN = "ضع_التوكن_هنا"

# إضافة نوع mime خاص للملفات
mimetypes.add_type("text/css", ".css", True)

# إعدادات PayPal
PAYPAL_CLIENT_ID = env("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = env("PAYPAL_SECRET")
PAYPAL_MODE = env("PAYPAL_MODE", default="live")  # استخدم "live" في الإنتاج

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# مفتاح الأمان
SECRET_KEY = env("SECRET_KEY", default="change-this-to-a-secure-key")

# وضع التصحيح
DEBUG = env.bool("DEBUG", default=True)

# السماح بالوصول
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['127.0.0.1', 'localhost', 'borouba-shop.onrender.com'])


# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',  # التطبيق الخاص بالمنتجات
    'rest_framework',
    'django_celery_beat',
    'django.contrib.humanize',
]

# الوسائط الوسطية (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ecommerce_project.middleware.RequestLoggingMiddleware',
]

# إعدادات عنوان URL الجذر
ROOT_URLCONF = 'ecommerce_project.urls'

# إعدادات القوالب (Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # مسار مجلد القوالب
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 'ecommerce_project.context_processors.cart_items',
                 'ecommerce_project.context_processors.site_settings_context',
            ],
        },
    },
]

# تطبيق WSGI
WSGI_APPLICATION = 'ecommerce_project.wsgi.application'




# التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# إعدادات اللغة والتوقيت
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# إعدادات الملفات الثابتة (Static Files)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"  # مسار الملفات الثابتة عند استخدام collectstatic
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# نوع المفتاح الافتراضي للحقول الأساسية
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# إعداد Celery لاستخدام Redis كوسيط للرسائل
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# إعدادات العملة
DEFAULT_CURRENCY = "USD"  # العملة الافتراضية
SUPPORTED_CURRENCIES = ["USD", "DZD"]  # العملات المدعومة

# سعر الصرف الحالي للدينار الجزائري مقابل الدولار (يجب تحديثه دوريًا)
EXCHANGE_RATE_DZD_TO_USD = 0.0073  # 1 DZD = 0.0073 USD

# إعدادات البريد الإلكتروني
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # استخدم SMTP الخاص بمزود الخدمة
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-email-password"
DEFAULT_FROM_EMAIL = "no-reply@yourstore.com"

# إعدادات الميديا
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# إعدادات ملفات السجل
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',  # عرض الأخطاء فقط
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',  # عرض الأخطاء فقط
            'propagate': True,
        },
    },
}

LOGIN_REDIRECT_URL = '/cart/'  # توجيه المستخدم إلى سلة التسوق بعد تسجيل الدخول
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = '/'  # توجيه المستخدم إلى صفحة تسجيل الدخول بعد تسجيل الخروج




