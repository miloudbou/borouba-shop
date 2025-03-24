import pytest
from django.contrib.auth.models import User
from products.models import Product

# Fixture لإنشاء مستخدم لاختباراتك
@pytest.fixture
def create_user():
    """Fixture لإنشاء مستخدم للاختبارات"""
    return User.objects.create_user(username='testuser', password='testpassword')

# Fixture لإنشاء منتج لاختباراتك
@pytest.fixture
def create_product():
    """Fixture لإنشاء منتج للاختبارات"""
    return Product.objects.create(
        name="Test Product",
        description="This is a test product.",
        price=100.0
    )