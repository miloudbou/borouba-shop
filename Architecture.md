# وثيقة هيكلية متقدمة لمشروع "بوروبة شوب"

## جدول المحتويات
1. [مقدمة](#مقدمة)
2. [نظرة عامة على الهندسة](#نظرة-عامة-على-الهندسة)
3. [مخطط هيكلي للمجلدات](#مخطط-هيكلي-للمجلدات)
4. [تفاصيل المكونات](#تفاصيل-المكونات)
   - 4.1 [database](#database)
   - 4.2 [ecommerce_project](#ecommerce_project)
   - 4.3 [products](#products)
   - 4.4 [templates](#templates)
   - 4.5 [static](#static)
5. [بيئات العمل والنشر](#بيئات-العمل-والنشر)
6. [أفضل الممارسات](#أفضل-الممارسات)
7. [المراجع](#المراجع)

---

## مقدمة
توثيق شامل لهيكلية مشروع "بوروبة شوب"، منصة تجارة إلكترونية مبنية على Django، Celery، وRedis، مع دمج تلقائي لمنتجات AliExpress. يهدف هذا المستند إلى:
- تسهيل صيانة وتطوير المشروع
- توجيه المطورين الجدد في فهم البنية العامة
- توضيح دورة حياة الطلب والبيانات

## نظرة عامة على الهندسة
- **Django (Backend):** إدارة النماذج، العروض، القوالب، والمصادقة.
- **Celery + Redis:** تنفيذ المهام الخلفية (جلب المنتجات، إرسال الإشعارات).
- **Front-End:** Bootstrap 5، FontAwesome، وAJAX لتحسين تجربة المستخدم.
- **Deployment:** حاويات Docker، Heroku (Procfile)، وGitHub Actions لـCI/CD.

## مخطط هيكلي للمجلدات
```text
ecommerce_project/         # جذر المشروع
├── database/              # سكربتات إدارة البيانات
├── ecommerce_project/     # إعدادات Django وCelery
├── products/              # تطبيق المنتجات والوظائف المرتبطة
├── templates/             # القوالب العامة والجزئية
├── static/                # الأصول الثابتة
├── tests/                 # اختبارات الوحدة (تُنصح الإضافة)
├── .env                   # متغيرات البيئة (سرية)
├── Dockerfile             # بناء Docker image
├── docker-compose.yml     # تشغيل الخدمات محليًا
├── Procfile               # ضبط Heroku
├── requirements.txt       # تبعيات Python
└── README.md              # نظرة عامة وتعليمات التشغيل
```

## تفاصيل المكونات

### 4.1 database
- **clean_products.py:** تنظيف وتحضير بيانات المنتجات.
- **database.py:** تكوين وتنفيذ اتصالات DB.
- **delete_products.py:** سكربت لحذف المنتجات غير المرغوب فيها.
- **queries.py:** SQL مخصص للاستعلامات المعقدة.

### 4.2 ecommerce_project
- **settings.py:** إعدادات Django (BASE_DIR, INSTALLED_APPS, MIDDLEWARE, Celery, Redis).
- **urls.py:** خرائط URL العامة.
- **asgi.py / wsgi.py:** واجهات الخادم.
- **celery.py:** إعداد Celery مع Broker وBackend.
- **context_processors.py:** إضافة البيانات المشتركة (`cart_count`, `user_profile`).
- **middleware.py:** معالجة الطلب (مثلاً: التحقق من IP، Logging).

### 4.3 products
- **models.py:** تعريف `Product`, `Category`, `ProductImage`, `Review`.
- **fetch_products.py:** جلب وتحديث المنتجات من AliExpress Open API.
- **tasks.py:** مهام مجدولة (تحديث يومي، إرسال إشعارات للمستخدمين).
- **signals.py:** معالجة ما بعد الحفظ (تحديث المخزون، سجل النشاط).
- **forms.py:** نماذج Django للبحث، السلة، والدفع.
- **serializers.py:** لدعم واجهات REST (اختياري).
- **views/**: منطق العرض مقسم إلى:
  - `product_views.py`
  - `category_views.py`
  - `cart_views.py`
  - `order_views.py`
  - `payment_views.py`
  - `auth_views.py`
  - `wishlist_views.py`
  - `admin_views.py`
- **urls.py:** مسارات التطبيق.
- **templates/products/**: قوالب HTML الخاصة بالتطبيق.

### 4.4 templates
- **base.html:** الهيكل العام (رأس، فوتر، `{% block content %}`).
- **partials/**: أجزاء قابلة للإعادة (`navbar.html`, `footer.html`, `head.html`, `scripts.html`, `messages.html`).
- **errors/**: قوالب الأخطاء (`404.html`, `500.html`).

### 4.5 static
- **vendor/**: مكتبات الطرف الثالث (Bootstrap، jQuery).
- **styles/**: تخصيصات CSS.
- **js/**: جافاسكربت مخصصة.
- **images/**: الأصول الثابتة (logos، defaults).

## بيئات العمل والنشر
- **Local Development:** Docker Compose (PostgreSQL, Redis, Django, Celery Worker).  
- **Production:** Heroku (Procfile)، اتصال بـ Redis وPostgreSQL من Add-ons.  
- **CI/CD:** GitHub Actions لتشغيل الاختبارات (pytest)، فحص الشيفرة (flake8، black)، وبناء Docker image.

## أفضل الممارسات
1. **الاختبارات:** إضافة مجلد `tests/` لكل تطبيق واستخدام pytest.
2. **التوثيق:** تحديث مستمر لـARCHITECTURE.md وREADME.md.
3. **نمط الكود:** الالتزام بـPEP8، Black للتنسيق.
4. **أمن:** استخدام django-environ لإدارة الأسرار، تأمين Headers باستخدام `django-secure`.
5. **المراقبة:** دمج Sentry لتتبع الأخطاء.

## المراجع
- [Django Documentation](https://docs.djangoproject.com/)  
- [Celery Documentation](https://docs.celeryproject.org/)  
- [Heroku Dev Center](https://devcenter.heroku.com/)

---

*ملف تم إنشاؤه بتاريخ 26 أبريل 2025*



