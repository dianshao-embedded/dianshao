# Generated by Django 2.2 on 2022-01-26 01:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20220123_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypackages',
            name='go_proxy',
            field=models.CharField(default=django.utils.timezone.now, max_length=120),
            preserve_default=False,
        ),
    ]
