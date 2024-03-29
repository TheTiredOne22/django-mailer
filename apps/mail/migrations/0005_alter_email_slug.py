# Generated by Django 4.2.10 on 2024-02-29 03:59

import apps.mail.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mail', '0004_rename_thread_email_parent_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='slug',
            field=models.SlugField(blank=True, default=apps.mail.models.uuid.uuid4, editable=False, max_length=16,
                                   unique=True),
        ),
    ]
