# Generated by Django 5.0 on 2024-01-17 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0004_rename_product_order_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
