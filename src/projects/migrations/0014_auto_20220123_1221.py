# Generated by Django 2.2 on 2022-01-23 12:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_mypackages_files_pn'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypackages',
            name='extra_oemake',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=60), default="{}", size=None),
            preserve_default=False,
        ),
    ]
