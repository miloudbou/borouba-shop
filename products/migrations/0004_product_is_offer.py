# Generated by Django 5.1.7 on 2025-03-25 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_paymentmethod_shipping_alter_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_offer',
            field=models.BooleanField(default=False),
        ),
    ]
