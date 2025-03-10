# Generated by Django 5.0.6 on 2024-06-11 15:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('boxes', '0005_box_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='memory',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
