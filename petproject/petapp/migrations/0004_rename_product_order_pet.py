# Generated by Django 5.0 on 2024-01-17 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0003_alter_pet_managers_cartpet_user_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='pet',
        ),
    ]
