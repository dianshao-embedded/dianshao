# Generated by Django 2.2 on 2022-03-16 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20220316_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='myimage',
            name='dishes_url',
            field=models.CharField(default='http://127.0.0.1:8080', max_length=100),
            preserve_default=False,
        ),
    ]