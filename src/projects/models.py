from re import T
from django import VERSION
from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    REMOTE_OR_LOCAL = [
        ('local', 'local'),
        ('remote', 'remote'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    remote_or_local = models.CharField(max_length=60, choices=REMOTE_OR_LOCAL)
    name = models.CharField(max_length=100)
    sub = models.CharField(max_length=100)

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
        # TODO: ('System-V', 'System-V')
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

    CATAGORY = [
        #('recipes-kernel', 'recipes-kernel'),
        #('recipes-bsp', 'recipes-bsp'),
        ('recipes-dianshao', 'recipes-dianshao'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=FILE_TYPE)
    catagory = models.CharField(max_length=100, choices=CATAGORY)
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
    source_directory = models.CharField(max_length=100)
    inherit = models.CharField(max_length=60)
    systemd_service_pn = models.CharField(max_length=120)
    config_file_path = models.CharField(max_length=120)
    go_env = ArrayField(models.CharField(max_length=120, blank=True))
    go_proxy = models.CharField(max_length=120)
    files_pn = ArrayField(models.CharField(max_length=120, blank=True))
    extra_oemake = ArrayField(models.CharField(max_length=60, blank=True))

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
    #TODO: 最大文件内容长度还需要优化
    content = models.CharField(max_length=20000)

class ExtraMarco(models.Model):
    package = models.ForeignKey(MyPackages, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    value = models.CharField(max_length=300)
    description = models.CharField(max_length=300)

    VALUE_SETTING_STRENGTH_LEVEL = [
        ('normal', 'normal'),
        ('weak', 'weak'),
        ('very weak', 'very weak'),
        ('append', 'append'),
    ]
    strength = models.CharField(max_length=100, 
                        choices=VALUE_SETTING_STRENGTH_LEVEL)

class MyMachine(models.Model):
    BASE = [
        ('imx6ull', 'imx6ull'),
        ('none', 'None'),
    ]

    INITIAL_METHOD = [
        ('Systemd', 'Systemd'),
        # TODO: ('System-V', 'System-V')
    ]

    FLASH = [
        ('Spi-Nor', 'Spi-Nor'),
        ('Rawnand', 'Rawnand'),
        #('EMMC', 'EMMC'),
        ('SDCard', 'SDCard'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=300)
    base = models.CharField(max_length=60, choices=BASE)
    machineoverrides = models.CharField(max_length=60, blank=True)
    # TODO: Add MACHINEOVERRIDES (后续要提供选项，通过BASE)
    # TODO: Add DEFAULTTUNE
    uboot = models.CharField(max_length=60, blank=True)
    uboot_defconfig = models.CharField(max_length=120, blank=True)
    kernel = models.CharField(max_length=60, blank=True)
    kernel_defconfig = models.CharField(max_length=120, blank=True)
    flash = models.CharField(max_length=60, choices=FLASH) # TODO：在view中根据芯片和板子选型动态加载选项
    filesystem = models.CharField(max_length=60, blank=True)
    initial_method = models.CharField(max_length=30, choices=INITIAL_METHOD)
    jffs2_eraseblock = models.CharField(max_length=30, blank=True)
    mkubifs_args = models.CharField(max_length=120, blank=True)
    ubinize_args = models.CharField(max_length=120, blank=True)
    mxsboot_nand_args = models.CharField(max_length=120, blank=True)
    machine_include = ArrayField(models.CharField(max_length=60, blank=True))
    distro_include = ArrayField(models.CharField(max_length=60, blank=True))
    distro_version = models.CharField(max_length=60, blank=True)
    kernel_dts = models.CharField(max_length=120, blank=True)

class MachineExtraMarco(models.Model):
    machine = models.ForeignKey(MyMachine, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    value = models.CharField(max_length=300)
    description = models.CharField(max_length=300)

    VALUE_SETTING_STRENGTH_LEVEL = [
        ('normal', 'normal'),
        ('weak', 'weak'),
        ('very weak', 'very weak'),
        ('append', 'append'),
    ]
    strength = models.CharField(max_length=100, 
                        choices=VALUE_SETTING_STRENGTH_LEVEL)

class MyImage(models.Model):
    IMAGE_BASE = [
        ('poky-minimal', 'poky-minimal'),
        ('poky-base', 'poky-base')
    ]

    FLASH = [
        ('Spi-Nor', 'Spi-Nor'),
        ('Rawnand', 'Rawnand'),
        #('EMMC', 'EMMC'),
        ('SDCard', 'SDCard'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    base = models.CharField(max_length=60, choices=IMAGE_BASE)
    description = models.CharField(max_length=300)
    flash = models.CharField(max_length=60, choices=FLASH)
    wic_file = models.CharField(max_length=120)
    uboot_name = models.CharField(max_length=30)
    uboot_start = models.CharField(max_length=30)
    uboot_end = models.CharField(max_length=30)
    kernel_name = models.CharField(max_length=30)
    kernel_start = models.CharField(max_length=30)
    kernel_end = models.CharField(max_length=30)
    fs_name = models.CharField(max_length=30)
    fs_start = models.CharField(max_length=30)
    fs_end = models.CharField(max_length=30)
    packages = ArrayField(models.CharField(max_length=60, blank=True))
    compatible = models.CharField(max_length=60)
    product_id = models.CharField(max_length=60)
    file_path = models.CharField(max_length=200)
    file_name = models.CharField(max_length=60)
    dishes_url = models.CharField(max_length=100)

    STAGE = [
        ('dev', 'dev')
    ]
    stage = models.CharField(max_length=10, choices=STAGE)

    version = models.CharField(max_length=60)
    fs_type = models.CharField(max_length=10)


class MyImagePackage(models.Model):
    image = models.ForeignKey(MyImage, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    version = models.CharField(max_length=60)
    
class MyImageExtraMarco(models.Model):
    image = models.ForeignKey(MyImage, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    value = models.CharField(max_length=300)
    description = models.CharField(max_length=300)

    VALUE_SETTING_STRENGTH_LEVEL = [
        ('normal', 'normal'),
        ('weak', 'weak'),
        ('very weak', 'very weak'),
        ('append', 'append'),
    ]
    strength = models.CharField(max_length=100, 
                        choices=VALUE_SETTING_STRENGTH_LEVEL)

class Upgrade(models.Model):
    image = models.ForeignKey(MyImage, on_delete=models.CASCADE)
    compatible = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    product_id = models.CharField(max_length=60)
    file_path = models.CharField(max_length=200)
    file_name = models.CharField(max_length=60)

    STAGE = [
        ('dev', 'dev')
    ]
    stage = models.CharField(max_length=10, choices=STAGE)

    version = models.CharField(max_length=60)

# TODO：my machine 需要根据使用的芯片来确定，这部分放到后面去做，先选择使用的芯片厂家，然后生成需要配置的宏
# 或者直接改成 my-uboot 和 my-kernel，根据 boot 和 kernel 的bbfile直接生成相应的宏
# 第一步还是将其作为文件系统制作工具，machine直接采用支持包做好的形式来，后续不断增加支持的芯片，可以根据芯片去灵活修改就行了
# My machine 包括uboot和内核，暂且不开放协助开发的功能，后续实现
# My Filesystem 包括文件系统制作，拉取哪些包等
# My Image 主要为镜像制作过程所需文件，及相关宏定义
