# Generated by Django 2.2 on 2021-12-22 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20211222_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypackages',
            name='donwload_method',
            field=models.CharField(choices=[('git', 'git'), ('wget', 'wget')], max_length=60),
        ),
        migrations.AlterField(
            model_name='mypackages',
            name='language',
            field=models.CharField(choices=[('C/C++', 'C/C++'), ('Golang', 'Golang')], max_length=60),
        ),
        migrations.AlterField(
            model_name='mypackages',
            name='type',
            field=models.CharField(choices=[('bbappend', 'bbappend'), ('bb', 'bb')], max_length=60),
        ),
    ]
