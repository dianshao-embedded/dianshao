# Generated by Django 2.2 on 2021-12-27 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20211227_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymachine',
            name='initial_method',
            field=models.CharField(choices=[('Systemd', 'Systemd')], max_length=30),
        ),
        migrations.AlterField(
            model_name='mypackages',
            name='initial_method',
            field=models.CharField(choices=[('Systemd', 'Systemd')], max_length=30),
        ),
    ]
