# Generated by Django 2.2 on 2022-01-18 09:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_mypackages_source_directory'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypackages',
            name='catagory',
            field=models.CharField(choices=[('recipes-kernel', 'recipes-kernel'), ('recipes-bsp', 'recipes-bsp'), ('recipes-dianshao', 'recipes-dianshao')], default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
