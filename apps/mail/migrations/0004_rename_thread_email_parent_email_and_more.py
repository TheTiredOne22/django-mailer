# Generated by Django 4.2.10 on 2024-02-27 09:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_alter_email_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='thread',
            new_name='parent_email',
        ),
        migrations.AddField(
            model_name='email',
            name='is_archived_by_recipient',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='is_archived_by_sender',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='is_deleted_by_recipient',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='is_deleted_by_sender',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='is_starred_by_recipient',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='is_starred_by_sender',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='email',
            name='slug',
            field=models.SlugField(blank=True, default=uuid.uuid4, editable=False, max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='subject',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='UserEmailActions',
        ),
    ]