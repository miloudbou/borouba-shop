import os
import mimetypes
from pathlib import Path
import environ

# =========================
# تحميل القيم من .env
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# =========================
# إعدادات أساسية
# =========================
SECRET_KEY = env("SECRET_KEY", default="change-this-to-a-secure-key")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['127.0.0.1', 'localhost', 'borouba-shop.onrender.com'])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://borouba-shop.onrender.com"])

# =========================
# التطبيقات المثبتة
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
    'rest_framework',
    'django_celery_beat',
    'django.contrib.humanize',
]

# =========================
# الوسائط الوسطية (Middleware)
# =========================
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

# =========================
# عنوان URL الجذر
# =========================
ROOT_URLCONF = 'ecommerce_project.urls'

# =========================
# إعدادات القوالب
# =========================
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
                'ecommerce_project.context_processors.site_settings_context',
            ],
        },
    },
]

# =========================
# تطبيق WSGI
# =========================
WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# =========================
# قاعدة البيانات
# =========================
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://localhost:5432/mydb?sslmode=require'),
}
DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

# =========================
# كلمات المرور
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# اللغة والتوقيت
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================
# الملفات الثابتة
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
mimetypes.add_type("text/css", ".css", True)

# =========================
# الميديا
# =========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# ملفات السجل
# =========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# =========================
# إعدادات Celery
# =========================
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# =========================
# إعدادات العملات
# =========================
DEFAULT_CURRENCY = "USD"
SUPPORTED_CURRENCIES = ["USD", "DZD"]
EXCHANGE_RATE_DZD_TO_USD = 0.0073

# =========================
# إعدادات البريد الإلكتروني
# =========================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="your-email@gmail.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="your-email-password")
DEFAULT_FROM_EMAIL = "no-reply@yourstore.com"

# =========================
# إعدادات تسجيل الدخول
# =========================
LOGIN_REDIRECT_URL = '/cart/'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = '/'

# =========================
# إعدادات الأمان الإضافية
# =========================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# =========================
# AliExpress API Settings
# =========================
ALIEXPRESS_CONFIG = {
    "API_URL": "https://api-sandbox.aliexpress.com",
    "APP_KEY": env("ALIEXPRESS_APP_KEY", default="ضع_المفتاح_هنا"),
    "SECRET": env("ALIEXPRESS_SECRET", default="ضع_السر_هنا"),
    "ACCESS_TOKEN": env("ALIEXPRESS_ACCESS_TOKEN", default="ضع_التوكن_هنا"),
}

# =========================
# PayPal Settings
# =========================
PAYPAL_CONFIG = {
    "CLIENT_ID": env("PAYPAL_CLIENT_ID"),
    "SECRET": env("PAYPAL_SECRET"),
    "MODE": env("PAYPAL_MODE", default="live"),
}

# =========================
# المفتاح الافتراضي للنماذج
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



