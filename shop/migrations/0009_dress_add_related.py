# Generated by Django 4.0.6 on 2022-08-03 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_models_bust_alter_models_firstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dress',
            name='add_related',
            field=models.TextField(blank=True, help_text='insert each item in one line', null=True, verbose_name='add related items'),
        ),
    ]
