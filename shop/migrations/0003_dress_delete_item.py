# Generated by Django 4.0.6 on 2022-08-03 06:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_delete_pricehistory_item_specefic_color_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
                ('quantity', models.PositiveIntegerField(help_text='the number of items left in the stock', verbose_name='quantity')),
                ('specefic_color', models.CharField(blank=True, max_length=100, null=True, verbose_name='specific color')),
                ('rate', models.CharField(default='0', max_length=4, verbose_name='rate')),
                ('rate_count', models.IntegerField(default=0, verbose_name='rate count')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='description')),
                ('features', models.TextField(blank=True, help_text='insert each feature in one line', null=True, verbose_name='features')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.brand', verbose_name='brand')),
                ('category', models.ManyToManyField(to='shop.category', verbose_name='category')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.color', verbose_name='color')),
                ('images', models.ManyToManyField(to='shop.itemimage', verbose_name='images')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.models', verbose_name='model')),
                ('related', models.ManyToManyField(to='shop.dress', verbose_name='related items')),
                ('sizeinfo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.clothesizeinfo')),
                ('sizes', models.ManyToManyField(to='shop.sizechoices', verbose_name='available sizes')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
