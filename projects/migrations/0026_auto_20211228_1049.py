# Generated by Django 2.2 on 2021-12-28 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_auto_20211228_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='myimage',
            name='max_parallel_threads',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myimage',
            name='parallel_make',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
