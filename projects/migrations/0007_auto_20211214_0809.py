# Generated by Django 2.2 on 2021-12-14 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20211214_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypackages',
            name='src_url',
            field=models.CharField(max_length=200),
        ),
    ]
