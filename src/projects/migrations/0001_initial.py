# Generated by Django 2.2 on 2022-01-05 02:48

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetaLayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('remote_or_local', models.CharField(choices=[('local', 'local'), ('remote', 'remote')], max_length=60)),
                ('name', models.CharField(max_length=100)),
                ('sub', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('base', models.CharField(choices=[('poky-minimal', 'poky-minimal'), ('poky-base', 'poky-base')], max_length=60)),
                ('description', models.CharField(max_length=300)),
                ('flash', models.CharField(choices=[('Spi-Nor', 'Spi-Nor'), ('Rawnand', 'Rawnand'), ('SDCard', 'SDCard')], max_length=60)),
                ('wic_file', models.CharField(max_length=120)),
                ('uboot_name', models.CharField(max_length=30)),
                ('uboot_start', models.CharField(max_length=30)),
                ('uboot_end', models.CharField(max_length=30)),
                ('kernel_name', models.CharField(max_length=30)),
                ('kernel_start', models.CharField(max_length=30)),
                ('kernel_end', models.CharField(max_length=30)),
                ('fs_name', models.CharField(max_length=30)),
                ('fs_start', models.CharField(max_length=30)),
                ('fs_end', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MyPackages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('bbappend', 'bbappend'), ('bb', 'bb')], max_length=30)),
                ('language', models.CharField(choices=[('C/C++', 'C/C++'), ('Golang', 'Golang')], max_length=30)),
                ('donwload_method', models.CharField(choices=[('git', 'git'), ('wget', 'wget'), ('local', 'local')], max_length=30)),
                ('initial_method', models.CharField(choices=[('Systemd', 'Systemd')], max_length=30)),
                ('version', models.CharField(max_length=100)),
                ('license_default', models.CharField(choices=[('MIT', 'MIT'), ('Apache-2.0', 'Apache-2.0'), ('BSD', 'BSD'), ('GPL-1.0-only', 'GPL-1.0-only'), ('GPL-2.0-only', 'GPL-2.0-only'), ('GPL-3.0-only', 'GPL-3.0-only'), ('CLOSED', 'CLOSED')], max_length=100)),
                ('license', models.CharField(max_length=100)),
                ('lic_files_chksum', models.CharField(max_length=150)),
                ('depends', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=150)),
                ('systemd_auto_enable', models.CharField(choices=[('enable', 'enable'), ('disable', 'disable')], max_length=60)),
                ('systemd_service_name', models.CharField(max_length=100)),
                ('section', models.CharField(max_length=50)),
                ('src_url', models.CharField(max_length=200)),
                ('src_rev', models.CharField(max_length=200)),
                ('src_url_md5', models.CharField(max_length=200)),
                ('src_url_sha256', models.CharField(max_length=200)),
                ('local_files', models.CharField(max_length=200)),
                ('files_install_directory', models.CharField(max_length=60)),
                ('building_directory', models.CharField(max_length=100)),
                ('inherit', models.CharField(max_length=60)),
                ('systemd_service_pn', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('project_path', models.CharField(max_length=150)),
                ('project_version', models.CharField(choices=[('ZEUS', 'zeus'), ('GATESGARTH', 'gatesgarth'), ('DUNFELL', 'dunfell'), ('HARDKNOTT', 'hardknott')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('do_configure', 'Configure'), ('do_compile', 'Compile'), ('do_install', 'Install')], max_length=60)),
                ('subtype', models.CharField(choices=[('prepend', 'Prepend'), ('none', 'None'), ('append', 'Append')], max_length=60)),
                ('op', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=150)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.MyPackages')),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('meta_layer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.MetaLayer')),
            ],
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Recipes')),
            ],
        ),
        migrations.AddField(
            model_name='mypackages',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.CreateModel(
            name='MyMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=300)),
                ('base', models.CharField(choices=[('imx6ull', 'imx6ull'), ('none', 'None')], max_length=60)),
                ('machineoverrides', models.CharField(max_length=60)),
                ('uboot', models.CharField(max_length=60)),
                ('uboot_defconfig', models.CharField(max_length=120)),
                ('kernel', models.CharField(max_length=60)),
                ('kernel_defconfig', models.CharField(max_length=120)),
                ('flash', models.CharField(choices=[('Spi-Nor', 'Spi-Nor'), ('Rawnand', 'Rawnand'), ('SDCard', 'SDCard')], max_length=60)),
                ('filesystem', models.CharField(max_length=60)),
                ('initial_method', models.CharField(choices=[('Systemd', 'Systemd')], max_length=30)),
                ('jffs2_eraseblock', models.CharField(max_length=30)),
                ('mkubifs_args', models.CharField(max_length=120)),
                ('ubinize_args', models.CharField(max_length=120)),
                ('mxsboot_nand_args', models.CharField(max_length=120)),
                ('machine_include', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=60), size=None)),
                ('distro_include', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=60), size=None)),
                ('distro_version', models.CharField(max_length=60)),
                ('kernel_dts', models.CharField(max_length=120)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='MyImagePackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=60)),
                ('version', models.CharField(max_length=60)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.MyImage')),
            ],
        ),
        migrations.AddField(
            model_name='myimage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.CreateModel(
            name='MyConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=150)),
                ('strength', models.CharField(choices=[('normal', 'normal'), ('weak', 'weak'), ('very weak', 'very weak'), ('append', 'append')], max_length=100)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
        migrations.AddField(
            model_name='metalayer',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.CreateModel(
            name='MachineExtraMarco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('value', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=300)),
                ('strength', models.CharField(choices=[('normal', 'normal'), ('weak', 'weak'), ('very weak', 'very weak'), ('append', 'append')], max_length=100)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.MyMachine')),
            ],
        ),
        migrations.CreateModel(
            name='LocalFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('type', models.CharField(max_length=30)),
                ('path', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=2000)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.MyPackages')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraMarco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('value', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=300)),
                ('strength', models.CharField(choices=[('normal', 'normal'), ('weak', 'weak'), ('very weak', 'very weak'), ('append', 'append')], max_length=100)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.MyPackages')),
            ],
        ),
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=100)),
                ('command', models.CharField(max_length=100)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
