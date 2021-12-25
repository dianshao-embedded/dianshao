from os import path
from django.db import models
from django.db.models.base import Model

# Create your models here.

class Project(models.Model):
    SURPPORT_YOCTO_VERSION = [
        ('ZEUS', 'zeus'),
        ('GATESGARTH', 'gatesgarth'),
        ('DUNFELL', 'dunfell'),
        ('HARDKNOTT', 'hardknott'),
    ]

    project_name = models.CharField(max_length=100)
    project_path = models.CharField(max_length=150)
    project_version = models.CharField(max_length=100, 
                        choices=SURPPORT_YOCTO_VERSION)


class MetaLayer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    name = models.CharField(max_length=100)

class Build(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    target = models.CharField(max_length=100)
    command = models.CharField(max_length=100)

class Recipes(models.Model):
    meta_layer = models.ForeignKey(MetaLayer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
class Packages(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class MyConf(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=150)
    
    VALUE_SETTING_STRENGTH_LEVEL = [
        ('normal', 'normal'),
        ('weak', 'weak'),
        ('very weak', 'very weak'),
        ('append', 'append'),
    ]
    strength = models.CharField(max_length=100, 
                        choices=VALUE_SETTING_STRENGTH_LEVEL)
    
class MyPackages(models.Model):
    # TODO: 将数据库修改为pgsql，使用其数组功能
    FILE_TYPE = [
        ('bbappend', 'bbappend'),
        ('bb', 'bb'),
    ]

    LANGUAGE = [
        ('C/C++', 'C/C++'),
        ('Golang', 'Golang'),
    ]

    DOWNLOAD_METHOD = [
        ('git', 'git'),
        ('wget', 'wget'),
        ('local', 'local'),
    ]

    INITIAL_METHOD = [
        ('Systemd', 'Systemd'),
        ('System-V', 'System-V')
    ]

    LICENSE_DEFAULT = [
        ('MIT', 'MIT'),
        ('Apache-2.0', 'Apache-2.0'),
        ('BSD', 'BSD'),
        ('GPL-1.0-only', 'GPL-1.0-only'),
        ('GPL-2.0-only', 'GPL-2.0-only'),
        ('GPL-3.0-only', 'GPL-3.0-only'),
        ('CLOSED', 'CLOSED'),
    ]

    SYSTEMD_AUTO_START = [
        ('enable', 'enable'),
        ('disable', 'disable'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=FILE_TYPE)
    language = models.CharField(max_length=30, choices=LANGUAGE)
    donwload_method = models.CharField(max_length=30, choices=DOWNLOAD_METHOD)
    initial_method = models.CharField(max_length=30, choices=INITIAL_METHOD)
    version = models.CharField(max_length=100)
    license_default = models.CharField(max_length=100, choices=LICENSE_DEFAULT)
    license = models.CharField(max_length=100)
    lic_files_chksum = models.CharField(max_length=150)
    depends = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    systemd_auto_enable = models.CharField(max_length=60, choices=SYSTEMD_AUTO_START)
    systemd_service_name = models.CharField(max_length=100)
    section = models.CharField(max_length=50)
    src_url = models.CharField(max_length=200)
    src_rev = models.CharField(max_length=200)
    src_url_md5 = models.CharField(max_length=200)
    src_url_sha256 = models.CharField(max_length=200)
    local_files = models.CharField(max_length=200)
    files_install_directory = models.CharField(max_length=60)
    building_directory = models.CharField(max_length=100)
    inherit = models.CharField(max_length=60)
    systemd_service_pn = models.CharField(max_length=120)

class Tasks(models.Model):
    TASKS_TYPE = [
        ('do_configure', 'Configure'),
        ('do_compile', 'Compile'),
        ('do_install', 'Install'),
    ]

    TASK_SUBTYPE = [
        ('prepend', 'Prepend'),
        ('none', 'None'),
        ('append', 'Append'),
    ]

    package = models.ForeignKey(MyPackages, on_delete=models.CASCADE)
    type = models.CharField(max_length=60, choices=TASKS_TYPE)
    subtype = models.CharField(max_length=60, choices=TASK_SUBTYPE)
    op = models.CharField(max_length=300)
    description = models.CharField(max_length=150)

class LocalFile(models.Model):
    package = models.ForeignKey(MyPackages, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=30)
    path = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)

class ExtraMarco(models.Model):
    package = models.ForeignKey(MyPackages, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    value = models.CharField(max_length=300)
    description = models.CharField(max_length=300)

# TODO：my machine 需要根据使用的芯片来确定，这部分放到后面去做，先选择使用的芯片厂家，然后生成需要配置的宏
# 或者直接改成 my-uboot 和 my-kernel，根据 boot 和 kernel 的bbfile直接生成相应的宏
# 第一步还是将其作为文件系统制作工具，machine直接采用支持包做好的形式来，后续不断增加支持的芯片，可以根据芯片去灵活修改就行了
# My machine 包括uboot和内核，暂且不开放协助开发的功能，后续实现
# My Filesystem 包括文件系统制作，拉取哪些包等
# My Image 主要为镜像制作过程所需文件，及相关宏定义