# Generated by Django 5.0.6 on 2024-06-11 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepicture',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/default_profile_picture.png', upload_to='profile_pictures'),
        ),
    ]