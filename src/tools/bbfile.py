import os
from tools.shell import shell_cmd
from projects.models import *

class DianshaoBBFile():
    def __init__(self, name, version, type):
        self.name = name
        self.version = version
        self.type = type
        self.bbfile = name + '_' + version + '.' + type
    
    def create_folder(self, project_path, recipes):
        meta_path = os.path.join(project_path, 'meta')
        if not os.path.exists(meta_path):
            os.mkdir(meta_path)
        
        recipes_path = os.path.join(meta_path, recipes)

        if not os.path.exists(recipes_path):
            os.mkdir(recipes_path)

        package_path = os.path.join(recipes_path, self.name)
        if not os.path.exists(package_path):
            os.mkdir(package_path)

        files_path = os.path.join(package_path, 'files')
        if not os.path.exists(files_path):
            os.mkdir(files_path)

        self.package_path = package_path
        self.files_path = files_path

    def create_bbfile(self, packageid):
        #TODO: 下一步需要更智能的生成 bbfile，例如用户只需告诉想要将某文件放置
        # 与莫文件夹下，无需像现在一样输入准确任务指令, install 部分重新实现下
        bbpath = os.path.join(self.package_path, self.bbfile)
        if os.path.exists(bbpath):
            os.remove(bbpath)
        
        package = MyPackages.objects.get(id=packageid)
        localfiles = LocalFile.objects.filter(package__id=packageid)
        tasks = Tasks.objects.filter(package__id=packageid).order_by('id')
        extraMarco = ExtraMarco.objects.filter(package__id=packageid)

        f = open(bbpath, 'w')
        f.write('# %s-%s\n' % (package.name, package.version))
        f.write('# Auto Generate by Dianshao\n')
        f.write('FILESEXTRAPATHS_prepend := "${THISDIR}/files:"\n')
        f.write('DESCRIPTION = "%s"\n' % package.description)
        if package.license_default != '':
            f.write('LICENSE = "%s"\n' % package.license_default)
            if package.license_default == 'MIT':
                f.write('LIC_FILES_CHKSUM = "%s"\n' % 
                    'file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302')
            elif package.license_default == 'Apache-2.0':
                f.write('LIC_FILES_CHKSUM = "%s"\n' %
                    'file://${COMMON_LICENSE_DIR}/Apache-2.0;md5=89aea4e17d99a7cacdbeed46a0096b10')
            elif package.license_default == 'BSD':
                f.write('LIC_FILES_CHKSUM = "%s"\n' %
                    'file://${COMMON_LICENSE_DIR}/BSD;md5=3775480a712fc46a69647678acb234cb')
            elif package.license_default == 'GPL-1.0-only':
                f.write('LIC_FILES_CHKSUM = "%s"\n' %
                    'file://${COMMON_LICENSE_DIR}/GPL-1.0-only;md5=e9e36a9de734199567a4d769498f743d')
            elif package.license_default == 'GPL-2.0-only':
                f.write('LIC_FILES_CHKSUM = "%s"\n' %
                    'file://${COMMON_LICENSE_DIR}/GPL-2.0-only;md5=801f80980d171dd6425610833a22dbe6')

            elif package.license_default == 'GPL-3.0-only':
                f.write('LIC_FILES_CHKSUM = "%s"\n' %
                    'file://${COMMON_LICENSE_DIR}/GPL-2.0-only;md5=c79ff39f19dfec6d293b95dea7b07891')
            else:
                pass
        else:
            if package.license != '':
                f.write('LICENSE = "%s"\n' % package.license)
            if package.lic_files_chksum != '':
                f.write('LIC_FILES_CHKSUM = "%s"\n' % package.lic_files_chksum)
        if package.depends != '':
            f.write('DEPENDS = "%s"\n' % package.depends)
        # f.write('FILES_$\{PN\} += "%s"\n' % package.files_install_directory)
        
        # generate SRC_URI
        if package.type == 'bb':
            f.write('SRC_URI = "\ \n')
            if package.src_url != '':
                f.write('\t%s \ \n' % package.src_url)
            for lf in localfiles:
                f.write('\tfile://%s \ \n' % lf.name)
            f.write('"\n')
        elif package.type == 'bbappend':
            f.write('SRC_URI_append = "\ \n')
            if package.src_url != '':
                f.write('\t%s \ \n' % package.src_url)
            for lf in localfiles:
                f.write('\tfile://%s \ \n' % lf.name)
            f.write('"\n')            

        if package.src_rev != '':
            f.write('SRCREV = "%s"\n' % package.src_rev)
        if package.src_url_sha256 != '':
            f.write('SRC_URI[sha256sum] = "%s"\n' % package.src_url_sha256)
        if package.src_url_md5 != '':
            f.write('SRC_URI[src_url_md5] = "%s"\n' % package.src_url_md5)

        if package.source_directory != '':
            f.write('S = "%s"\n' % package.source_directory)

        """
        if package.building_directory != '':
            f.write('B = "%s"\n' % package.building_directory)
        """
        
        # generate inherit
        if package.initial_method == 'Systemd':
            if package.language == 'Golang':
                f.write('inherit systemd goarch\n')
            else:
                f.write('inherit systemd\n')
            f.write('SYSTEMD_AUTO_ENABLE = "%s"\n' % package.systemd_auto_enable)
            f.write('SYSTEMD_SERVICE_${PN} = "%s"\n' % package.systemd_service_name)
        elif package.initial_method == 'System-V':
            if package.language == 'Golang':
                f.write('inherit update-rc.d goarch\n')
            else:
                f.write('inherit update-rc.d\n')

        if package.language == 'Golang':
            f.write('export HOME = "${WORKDIR}"\n')
            f.write('export GOOS = "${TARGET_GOOS}"\n')
            f.write('export GOARCH = "${TARGET_GOARCH}"\n')
            f.write('export GOARM = "${TARGET_GOARM}"\n')
            f.write('export GOCACHE = "${WORKDIR}/go/cache"\n')

            if package.go_proxy != '':
                f.write('export GOPROXY = "%s"\n' % package.go_proxy)
                
            for env in package.go_env:
                f.write('export %s\n' % env)
        
        for eo in package.extra_oemake:
            f.write('EXTRA_OEMAKE += "%s"\n' % eo)

        if package.config_file_path != '':
            f.write('CONFFILES_${PN} = "%s"\n' % package.config_file_path)

        for file_pn in package.files_pn:
            f.write('FILES_${PN} += "%s"\n' % file_pn)

        for em in extraMarco:
            if em.strength == 'normal':
                f.write('%s = %s\n' % (em.name, em.value))
            elif em.strength == 'weak':
                f.write('%s ?= %s\n' % (em.name, em.value))
            elif em.strength == 'very weak':
                f.write('%s ??= %s\n' % (em.name, em.value))
            elif em.strength == 'append':
                f.write('%s += %s\n' % (em.name, em.value))                    

        do_configure_prepend = []
        do_configure = []
        do_configure_append = []
        do_compile_prepend = []
        do_compile = []
        do_compile_append = []
        do_install_prepend = []
        do_install = []
        do_install_append = []

        for task in tasks:
            if task.type == 'do_configure':
                if task.subtype == 'prepend':
                    do_configure_prepend.append(task.op)
                elif task.subtype == 'none':
                    do_configure.append(task.op)
                elif task.subtype == 'append':
                    do_configure_append.append(task.op)
            
            elif task.type == 'do_compile':
                if task.subtype == 'prepend':
                    do_compile_prepend.append(task.op)
                elif task.subtype == 'none':
                    do_compile.append(task.op)
                elif task.subtype == 'append':
                    do_compile_append.append(task.op)
            
            elif task.type == 'do_install':
                if task.subtype == 'prepend':
                    do_install_prepend.append(task.op)
                elif task.subtype == 'none':
                    do_install.append(task.op)
                elif task.subtype == 'append':
                    do_install_append.append(task.op)

        if len(do_configure_prepend) > 0:
            f.write('do_configure_prepend () {\n')
            for op in do_configure_prepend:
                f.write('\t%s\n' % op)
            f.write('}\n')

        if len(do_configure) > 0:
            f.write('do_configure () {\n')
            for op in do_configure:
                f.write('\t%s\n' % op)
            f.write('}\n')

        if len(do_configure_append) > 0:
            f.write('do_configure_append () {\n')
            for op in do_configure_append:
                f.write('\t%s\n' % op)
            f.write('}\n')

        if len(do_compile_prepend) > 0:
            f.write('do_compile_prepend () {\n')
            for op in do_compile_prepend:
                f.write('\t%s\n' % op)
            f.write('}\n')

        if len(do_compile) > 0:
            f.write('do_compile () {\n')
            for op in do_compile:
                f.write('\t%s\n' % op)
            f.write('}\n')

        if len(do_compile_append) > 0:
            f.write('do_compile_append () {\n')
            for op in do_compile_append:
                f.write('\t%s\n' % op)
            f.write('}\n')

        if len(do_install_prepend) > 0:
            f.write('do_install_prepend () {\n')
            for op in do_install_prepend:
                f.write('\t%s\n' % op)
            f.write('}\n')

        if len(do_install) > 0:
            f.write('do_install () {\n')
            for op in do_install:
                f.write('\t%s\n' % op)
            f.write('}\n')

        if len(do_install_append) > 0:
            f.write('do_install_append () {\n')
            for op in do_install_append:
                f.write('\t%s\n' % op)
            f.write('}\n')

        f.close()

    def import_local_file(self, path, name):
        ret, err = shell_cmd('cp %s %s' % (os.path.join(path, name), self.files_path), path)
        if err:
            raise Exception(ret)

    def create_local_file(self, name, content):
        WINDOWS_LINE_ENDING = b'\r\n'
        UNIX_LINE_ENDING = b'\n'
        f = open(os.path.join(self.files_path, name), "w")
        f.write(content)
        f.close()

        file_path = os.path.join(self.files_path, name)
        with open(file_path, 'rb') as open_file:
            content = open_file.read()
    
        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

        with open(file_path, 'wb') as open_file:
            open_file.write(content)
            open_file.close()

class DianshaoMachineFile():
    
    def __init__(self, machine_id):
        self.machine = MyMachine.objects.get(id=machine_id)
        pass

    def create_machine_file(self):
        machine_path = os.path.join(self.machine.project.project_path, 
                    self.machine.project.project_name, 
                    'meta/conf/machine', self.machine.name+'.conf')
        if os.path.exists(machine_path):
            os.remove(machine_path)

        extraMarco = MachineExtraMarco.objects.filter(machine__id=self.machine.id)

        f = open(machine_path, 'w')
        f.write('# %s-%s\n' % (self.machine.name, self.machine.description))
        f.write('# Auto Generate by Dianshao\n')

        for i in self.machine.machine_include:
            f.write('include %s\n' % i)
        if self.machine.base == 'imx6ull':
            f.write('MACHINEOVERRIDES =. "mx6:mx6ull:"\n')
            f.write('ACCEPT_FSL_EULA = "1"\n')
            f.write('UBOOT_SUFFIX = "imx"\n')
            f.write('UBOOT_MAKE_TARGET = "u-boot.imx"\n')
            if self.machine.flash == 'Spi-Nor':
                f.write('UBOOT_CONFIG = "qspi1"\n')
                f.write('UBOOT_CONFIG[qspi1] = "%s"\n' % self.machine.uboot_defconfig)
            elif self.machine.flash == 'Rawnand':
                f.write('UBOOT_CONFIG = "nand"\n')
                f.write('UBOOT_CONFIG[nand] = "%s,ubifs"\n' % self.machine.uboot_defconfig)
            elif self.machine.flash == 'EMMC':
                f.write('UBOOT_CONFIG = "emmc"\n')
                f.write('UBOOT_CONFIG[emmc] = "%s,sdcard"\n' % self.machine.uboot_defconfig)
            elif self.machine.flash == 'SDCard':
                f.write('UBOOT_CONFIG = "sd"\n')
                if self.machine.uboot_defconfig != '':
                    f.write('UBOOT_CONFIG[sd] = "%s,sdcard"\n' % self.machine.uboot_defconfig)
        else:
            if self.machine.machineoverrides != '':
                f.write('MACHINEOVERRIDES =. "%s"\n' % self.machine.machineoverrides)
            if self.machine.uboot_defconfig != '':
                f.write('UBOOT_MACHINE = "%s"\n' % self.machine.uboot_defconfig)

        if self.machine.uboot != '':
            f.write('PREFERRED_PROVIDER_virtual/bootloader = "%s"\n' % self.machine.uboot)
            f.write('PREFERRED_PROVIDER_u-boot = "%s"\n' % self.machine.uboot)

        if self.machine.kernel != '':
            f.write('PREFERRED_PROVIDER_virtual/kernel = "%s"\n' % self.machine.kernel)

        if self.machine.kernel_defconfig != '':
            f.write('KBUILD_DEFCONFIG = "%s"\n' % self.machine.kernel_defconfig)
    
        if self.machine.kernel_dts != '':
            f.write('KERNEL_DEVICETREE = "%s"\n' % self.machine.kernel_dts)

        f.write('IMAGE_FSTYPES += "%s"\n' % self.machine.filesystem)

        if self.machine.jffs2_eraseblock != '':
            f.write('JFFS2_ERASEBLOCK = "%s"\n' % self.machine.jffs2_eraseblock)
        
        if self.machine.mkubifs_args != '':
            f.write('MKUBIFS_ARGS = "%s"\n' % self.machine.mkubifs_args)
        if self.machine.ubinize_args != '':
            f.write('UBINIZE_ARGS = "%s"\n' % self.machine.ubinize_args)
        if self.machine.mxsboot_nand_args != '':
            f.write('MXSBOOT_NAND_ARGS = "%s"\n' % self.machine.mxsboot_nand_args)
        for em in extraMarco:
            if em.strength == 'normal':
                f.write('%s = %s\n' % (em.name, em.value))
            elif em.strength == 'weak':
                f.write('%s ?= %s\n' % (em.name, em.value))
            elif em.strength == 'very weak':
                f.write('%s ??= %s\n' % (em.name, em.value))
            elif em.strength == 'append':
                f.write('%s += %s\n' % (em.name, em.value))

        f.close()   

    def create_distro_file(self):
        distro_path = os.path.join(self.machine.project.project_path, 
            self.machine.project.project_name, 
            'meta/conf/distro', self.machine.name+'.conf')
        if os.path.exists(distro_path):
            os.remove(distro_path)

        f = open(distro_path, 'w')
        f.write('# %s-%s\n' % (self.machine.name, self.machine.description))
        f.write('# Auto Generate by Dianshao\n')

        for i in self.machine.distro_include:
            f.write('include %s\n' % i)

        f.write('DISTRO = "%s"\n' % self.machine.name)
        f.write('DISTRO_NAME = "%s"\n' % self.machine.name)
        # TODO: add distro version
        f.write('DISTRO_VERSION = "1.0.0"\n')

        if self.machine.initial_method == 'Systemd':
            f.write('DISTRO_FEATURES_append = " systemd"\n')
            f.write('VIRTUAL-RUNTIME_init_manager = "systemd"\n')

        f.close()


class DianshaoImageFile():
    def __init__(self, image_id):
        self.image = MyImage.objects.get(id=image_id)

    def create_image_file(self):
        image_path = os.path.join(self.image.project.project_path, 
                    self.image.project.project_name, 
                    'meta/recipes-core/images', self.image.name+'.bb')
        if os.path.exists(image_path):
            os.remove(image_path)

        extraMarco = MyImageExtraMarco.objects.filter(image__id=self.image.id)

        f = open(image_path, 'w')
        f.write('# %s-%s\n' % (self.image.name, self.image.description))
        f.write('# Auto Generate by Dianshao\n') 

        if self.image.base == 'poky-minimal':
            f.write('require recipes-core/images/core-image-minimal.bb\n')
        elif self.image.base == 'poky-base':
            f.write('require recipes-core/images/core-image-base.bb\n')

        f.write('inherit extrausers\n')
        f.write('EXTRA_USERS_PARAMS = "usermod -P root root;"\n')

        if self.image.wic_file != "":
            f.write('WKS_FILE = "%s"\n' % self.image.wic_file)

        for package in self.image.packages:
            f.write('IMAGE_INSTALL += "%s"\n' % package)

        for em in extraMarco:
            if em.strength == 'normal':
                f.write('%s = %s\n' % (em.name, em.value))
            elif em.strength == 'weak':
                f.write('%s ?= %s\n' % (em.name, em.value))
            elif em.strength == 'very weak':
                f.write('%s ??= %s\n' % (em.name, em.value))
            elif em.strength == 'append':
                f.write('%s += %s\n' % (em.name, em.value))
                
        f.close()


class DianshaoConfFile():
    def __init__(self, project_id):
        self.project = Project.objects.get(id=project_id)

    def set_config_file(self, machine, distro, pm, pt):
        build_conf_path = os.path.join(self.project.project_path, 
            self.project.project_name, 'build/conf/local.conf')

        if os.path.exists(build_conf_path):
            content = open(build_conf_path, 'r')
            lines = content.readlines()
            lines[0] = ('DISTRO = "%s"\n' % distro)
            lines[1] = ('MACHINE = "%s"\n' % machine)
            for i in range(len(lines)):
                if lines[i].startswith('BB_NUMBER_THREADS') == True:
                    lines[i] = ('BB_NUMBER_THREADS = "%s"\n' % pt)
                elif lines[i].startswith('PARALLEL_MAKE') == True:
                    lines[i] = ('PARALLEL_MAKE = "-j %s"\n' % pm)

            content = open(build_conf_path, 'w')
            content.writelines(lines)
            content.close()

        sample_conf_path = os.path.join(self.project.project_path, 
            self.project.project_name, 'meta/conf/local.conf.sample')

        if os.path.exists(sample_conf_path):
            content = open(sample_conf_path, 'r')
            lines = content.readlines()
            lines[0] = ('DISTRO = "%s"\n' % distro)
            lines[1] = ('MACHINE = "%s"\n' % machine)
            
            for i in range(len(lines)):
                if lines[i].startswith('BB_NUMBER_THREADS') == True:
                    lines[i] = ('BB_NUMBER_THREADS = "%s"\n' % pt)
                elif lines[i].startswith('PARALLEL_MAKE') == True:
                    lines[i] = ('PARALLEL_MAKE = "-j %s"\n' % pm)

            content = open(sample_conf_path, 'w')
            content.writelines(lines)
            content.close()
        
class DianshaoWksFile():
    def __init__(self, project_id):
        self.project = Project.objects.get(id=project_id)

    def create(self, name, content):
        file_path = os.path.join(self.project.project_path, 
                    self.project.project_name, 'meta/wic')
        
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        WINDOWS_LINE_ENDING = b'\r\n'
        UNIX_LINE_ENDING = b'\n'
        f = open(os.path.join(file_path, name), "w")
        f.write(content)
        f.close()

        file_path = os.path.join(file_path, name)
        with open(file_path, 'rb') as open_file:
            content = open_file.read()
    
        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

        with open(file_path, 'wb') as open_file:
            open_file.write(content)
            open_file.close()