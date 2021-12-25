import os
from tools.shell import shell_cmd
from projects.models import ExtraMarco, LocalFile, MyPackages, Tasks

class DianshaoBBFile():
    def __init__(self, name, version, type):
        self.name = name
        self.version = version
        self.type = type
        self.bbfile = name + '_' + version + '.' + type
    
    def create_folder(self, project_path):
        meta_path = os.path.join(project_path, 'meta')
        if not os.path.exists(meta_path):
            os.mkdir(meta_path)
        
        recipes_path = os.path.join(meta_path, 'recipes-dianshao')
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
        if package.license_default is not '':
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
            f.write('LICENSE = "%s"\n' % package.license)
            if package.lic_files_chksum is not '':
                f.write('LIC_FILES_CHKSUM = "%s"\n' % package.lic_files_chksum)
        if package.depends is not '':
            f.write('DEPENDS = "%s"\n' % package.depends)
        # f.write('FILES_$\{PN\} += "%s"\n' % package.files_install_directory)
        
        # generate SRC_URI
        if package.type == 'bb':
            f.write('SRC_URI = "\ \n')
            if package.src_url is not '':
                f.write('\t%s \ \n' % package.src_url)
            for lf in localfiles:
                f.write('\tfile://%s \ \n' % lf.name)
            f.write('"\n')
        elif package.type == 'bbappend':
            f.write('SRC_URI_append = "\ \n')
            if package.src_url is not '':
                f.write('\t%s \ \n' % package.src_url)
            for lf in localfiles:
                f.write('\tfile://%s \ \n' % lf.name)
            f.write('"\n')            

        if package.src_rev is not '':
            f.write('SRCREV = "%s"\n' % package.src_rev)
        if package.src_url_sha256 is not '':
            f.write('SRC_URI[sha256sum] = "%s"\n' % package.src_url_sha256)
        if package.src_url_md5 is not '':
            f.write('SRC_URI[src_url_md5] = "%s"\n' % package.src_url_md5)

        if package.building_directory is not '':
            f.write('S = "%s"\n' % package.building_directory)

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
            f.write('export GOOS = "${TARGET_GOOS}"\n')
            f.write('export GOARCH = "${TARGET_GOARCH}"\n')
            f.write('export GOARM = "${TARGET_GOARM}"\n')
            f.write('export GOCACHE = "${WORKDIR}/go/cache"\n')

        for em in extraMarco:
            f.write('%s = %s\n' % (em.name, em.value))

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
        f = open(os.path.join(self.files_path, name), "w")
        f.write(content)