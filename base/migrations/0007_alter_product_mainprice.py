# Generated by Django 4.1.7 on 2024-02-17 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_product_mainprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='mainprice',
            field=models.IntegerField(default=1),
        ),
    ]
