# Generated by Django 2.2 on 2021-12-28 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_myimagepackage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myimage',
            old_name='machine_id',
            new_name='machine',
        ),
    ]
