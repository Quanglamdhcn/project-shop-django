# Generated by Django 2.1.7 on 2019-05-08 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20190508_2035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
    ]
