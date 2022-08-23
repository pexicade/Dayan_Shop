# Generated by Django 4.0.6 on 2022-08-18 16:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_delete_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='testItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('page_title', models.CharField(blank=True, max_length=150, null=True, verbose_name='page title')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
                ('quantity', models.PositiveIntegerField(help_text='the number of items left in the stock', verbose_name='quantity')),
                ('specific_color', models.CharField(blank=True, max_length=100, null=True, verbose_name='specific color')),
                ('rate', models.CharField(default='0', max_length=4, verbose_name='rate')),
                ('rate_count', models.IntegerField(default=0, verbose_name='rate count')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('testfield', models.CharField(max_length=100)),
                ('category', models.ManyToManyField(to='shop.category', verbose_name='category')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.color', verbose_name='color')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
