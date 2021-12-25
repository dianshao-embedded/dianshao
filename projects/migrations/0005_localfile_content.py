# Generated by Django 2.2 on 2021-12-13 11:10

from django.db import migrations
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_localfile_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='localfile',
            name='content',
            field=tinymce.models.HTMLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
