# Generated by Django 4.0.6 on 2022-08-19 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.JSONField(blank=True, default={}, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='items_detail',
            field=models.JSONField(blank=True, default={}),
        ),
    ]
