# Generated by Django 4.0.6 on 2022-08-03 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_models_quick_add'),
    ]

    operations = [
        migrations.AlterField(
            model_name='models',
            name='bust',
            field=models.CharField(blank=True, max_length=120, verbose_name='bust'),
        ),
        migrations.AlterField(
            model_name='models',
            name='firstname',
            field=models.CharField(blank=True, max_length=120, verbose_name='fist name'),
        ),
        migrations.AlterField(
            model_name='models',
            name='height',
            field=models.CharField(blank=True, max_length=120, verbose_name='height'),
        ),
        migrations.AlterField(
            model_name='models',
            name='hip',
            field=models.CharField(blank=True, max_length=120, verbose_name='hip'),
        ),
        migrations.AlterField(
            model_name='models',
            name='lastname',
            field=models.CharField(blank=True, max_length=120, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='models',
            name='waist',
            field=models.CharField(blank=True, max_length=120, verbose_name='waist'),
        ),
        migrations.AlterField(
            model_name='models',
            name='weight',
            field=models.CharField(blank=True, max_length=120, verbose_name='weight'),
        ),
    ]