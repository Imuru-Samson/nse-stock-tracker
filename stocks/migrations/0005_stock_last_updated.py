# Generated by Django 4.2.21 on 2025-06-10 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_stock_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
