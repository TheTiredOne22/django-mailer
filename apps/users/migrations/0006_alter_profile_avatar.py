# Generated by Django 4.2.10 on 2024-02-18 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_address_alter_profile_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='media/profile_images'),
        ),
    ]