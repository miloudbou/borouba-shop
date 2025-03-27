import os
from pathlib import Path
from environ import Env  # مكتبة لإدارة المتغيرات البيئية

# ==========================
# إعدادات المشروع الأساسية
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

# إعداد المتغيرات البيئية
env = Env()
Env.read_env(os.path.join(BASE_DIR, '.env'))  # تحميل المتغيرات من ملف .env

SECRET_KEY = env("SECRET_KEY", default="change-this-to-a-secure-key")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['127.0.0.1', 'localhost', 'borouba-shop.onrender.com'])

# ==========================
# إعدادات التطبيقات
# ==========================
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
]

# ==========================
# إعدادات الوسائط الوسطية (Middleware)
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ecommerce_project.middleware.RequestLoggingMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# ==========================
# إعدادات القوالب (Templates)
# ==========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ecommerce_project.context_processors.cart_items',
            ],
        },
    },
]

# ==========================
# إعدادات قواعد البيانات
# ==========================
DATABASES = {
    'default': env.db(default="postgresql://bouroubashop:miloud1982@localhost:5432/ecommerce_db")
}


# ==========================
# إعدادات اللغة والتوقيت
# ==========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==========================
# إعدادات الملفات الثابتة والميديا
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================
# إعدادات تسجيل الدخول والخروج
# ==========================
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = '/cart/'

# ==========================
# إعدادات CSRF
# ==========================
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True

# ==========================
# إعدادات السجل (Logging)
# ==========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# ==========================
# إعدادات AliExpress API
# ==========================
ALIEXPRESS_API_URL = "https://api-sandbox.aliexpress.com"
ALIEXPRESS_APP_KEY = env("ALIEXPRESS_APP_KEY", default="ضع_المفتاح_هنا")
ALIEXPRESS_SECRET = env("ALIEXPRESS_SECRET", default="ضع_السر_هنا")
ALIEXPRESS_ACCESS_TOKEN = env("ALIEXPRESS_ACCESS_TOKEN", default="ضع_التوكن_هنا")

# ==========================
# إعدادات PayPal
# ==========================
PAYPAL_CLIENT_ID = env("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = env("PAYPAL_SECRET")
PAYPAL_MODE = env("PAYPAL_MODE", default="live")

# ==========================
# إعدادات Celery
# ==========================
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# ==========================
# إعدادات العملة
# ==========================
DEFAULT_CURRENCY = "USD"
SUPPORTED_CURRENCIES = ["USD", "DZD"]
EXCHANGE_RATE_DZD_TO_USD = 0.0073  # 1 DZD = 0.0073 USD

# ==========================
# إعدادات البريد الإلكتروني
# ==========================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="your-email@gmail.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="your-email-password")
DEFAULT_FROM_EMAIL = "no-reply@yourstore.com"

ROOT_URLCONF = 'ecommerce_project.urls'

