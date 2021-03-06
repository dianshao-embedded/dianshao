# Generated by Django 2.2 on 2022-03-16 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_mypackages_go_proxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='myimage',
            name='compatible',
            field=models.CharField(default='', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myimage',
            name='file_name',
            field=models.CharField(default='', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myimage',
            name='file_path',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myimage',
            name='fs_type',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myimage',
            name='product_id',
            field=models.CharField(default='', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myimage',
            name='stage',
            field=models.CharField(choices=[('dev', 'dev')], default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myimage',
            name='version',
            field=models.CharField(default='', max_length=60),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Upgrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compatible', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=60)),
                ('product_id', models.CharField(max_length=60)),
                ('file_path', models.CharField(max_length=200)),
                ('file_name', models.CharField(max_length=60)),
                ('stage', models.CharField(choices=[('dev', 'dev')], max_length=10)),
                ('version', models.CharField(max_length=60)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.MyImage')),
            ],
        ),
    ]
