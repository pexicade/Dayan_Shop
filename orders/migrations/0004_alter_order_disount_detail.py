# Generated by Django 4.0.6 on 2022-08-19 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_address_alter_order_items_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='disount_detail',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]