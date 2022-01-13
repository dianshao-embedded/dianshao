import json
import os
from pyexpat import model
from unicodedata import name
from projects.models import *

class Migration():

    def __init__(self):
        pass

    def project_export(self, project_id):
        project = Project.objects.get(id=project_id)
        project_dict = project.__dict__
        project_dict.pop('_state')

        metas = MetaLayer.objects.filter(project__id=project_id)
        metas_dict = []
        for m in metas:
            m_dict = m.__dict__
            m_dict.pop('_state')
            metas_dict.append(m_dict)

        mypackages = MyPackages.objects.filter(project__id=project_id)
        packages_dict = []
        for p in mypackages:
            p_dict = p.__dict__
            p_dict.pop('_state')
            tasks = Tasks.objects.filter(package__id=p.id)
            tasks_dict = []
            for t in tasks:
                t_dict = t.__dict__
                t_dict.pop('_state')
                tasks_dict.append(t_dict)

            localfiles = LocalFile.objects.filter(package__id=p.id)
            localfiles_dict = []
            for l in localfiles:
                l_dict = l.__dict__
                l_dict.pop('_state')
                localfiles_dict.append(l_dict)

            extramarcos = ExtraMarco.objects.filter(package__id=p.id)
            extramarcos_dict = []
            for e in extramarcos:
                e_dict = e.__dict__
                e_dict.pop('_state')
                extramarcos_dict.append(e_dict)

            p_dict['tasks'] = tasks_dict
            p_dict['localfiles'] = localfiles_dict
            p_dict['extramarcos'] = extramarcos_dict

            packages_dict.append(p_dict)

        mymachine = MyMachine.objects.get(project__id=project_id)
        mymachine_dict = mymachine.__dict__
        mymachine_dict.pop('_state')
        
        extramarcos = MachineExtraMarco.objects.filter(machine__id=mymachine.id)
        extramarcos_dict = []
        for e in extramarcos:
            e_dict = e.__dict__
            e_dict.pop('_state')
            extramarcos_dict.append(e_dict)
        
        mymachine_dict['extramarcos'] = extramarcos_dict

        myimages = MyImage.objects.filter(project__id=project_id)
        images_dict = []
        for i in myimages:
            i_dict = i.__dict__
            i_dict.pop('_state')
            packages = MyImagePackage.objects.filter(image__id=i.id)
            packages_dict = []
            for p in packages:
                p_dict = p.__dict__
                p_dict.pop('_state')
                packages_dict.append(p_dict)
            
            i_dict['packages'] = packages_dict

            images_dict.append(i_dict)

        project_dict['metas'] = metas_dict
        project_dict['mypackages'] = packages_dict
        project_dict['mymachine'] = mymachine_dict
        project_dict['myimages'] = images_dict

        file_path = os.path.join(project.project_path, 
                            project.project_name, 'dianshao_migration.json')

        if os.path.exists(file_path):
            os.remove(file_path)

        f = open(file_path, 'w')
        json.dump(project_dict, f)

    def project_import(self, project_path, project_name):
        file_path = os.path.join(project_path, 
                    project_name, 'dianshao_migration.json')

        if os.path.exists(file_path)== False:
            raise Exception("%s project is not a dianshao project" % project_name)
        
        f = open(file_path, 'r')
        project_dict = json.load(f)

        project = Project.objects.create(project_name=project_name, 
                                        project_path = project_path,
                                        project_version = project_dict['project_version'])
        
        for m in project_dict['metas']:
            MetaLayer.objects.create(project=project, url=m['url'], 
                            remote_or_local=m['remote_or_local'], name=m['name'], sub=m['sub'])

        for p in project_dict['mypackages']:
            package = Packages.objects.create(project=project, name=p['name'], type=p['type'], language=p['language'],
                            donwload_method=p['donwload_method'], initial_method=p['initial_method'], 
                            version=p['version'], license_default=p['license_default'], license=p['license'],
                            lic_files_chksum=p['lic_files_chksum'], depends=p['depends'], description=p['description'],
                            systemd_auto_enable=p['systemd_auto_enable'], systemd_service_name=p['systemd_service_name'],
                            section=p['section'], src_url=p['src_url'], src_rev=p['src_rev'], src_url_md5=p['src_url_md5'],
                            src_url_sha256=p['src_url_sha256'], local_files=p['local_files'], 
                            files_install_directory=p['files_install_directory'], building_directory=p['building_directory'],
                            inherit=p['inherit'], systemd_service_pn=p['systemd_service_pn'])

            for t in p['tasks']:
                Tasks.objects.create(package=package, type=t['type'], subtype=t['subtype'], op=t['op'], description=t['description'])

            for l in p['localfiles']:
                LocalFile.objects.create(package=package, name=l['name'], type=l['type'], path=l['path'], content=l['content'])

            for e in p['extramarcos']:
                ExtraMarco.objects.create(package=package, name=e['name'], value=e['value'], description=e['description'], strength=e['strength'])

        m = project_dict['mymachine']
        machine = MyMachine.objects.create(project=project, name=m['name'], description=m['description'], base=m['base'],
                                    machineoverrides=m['machineoverrides'], uboot=m['uboot'], uboot_defconfig=m['uboot_defconfig'],
                                    kernel=m['kernel'], kernel_defconfig=m['kernel_defconfig'], flash=m['flash'], filesystem=m['filesystem'],
                                    initial_method=m['initial_method'], jffs2_eraseblock=m['jffs2_eraseblock'], mkubifs_args=m['mkubifs_args'],
                                    ubinize_args=m['ubinize_args'], mxsboot_nand_args=m['mxsboot_nand_args'], machine_include=m['machine_include'],
                                    distro_include=m['distro_include'], distro_version=m['distro_version'], kernel_dts=m['kernel_dts'])

        for e in m['extramarcos']:
            MachineExtraMarco.objects.create(machine=machine, name=e['name'], value=e['value'], description=e['description'], strength=e['strength'])

        for i in project_dict['myimages']:
            image = MyImage.objects.create(project=project, name=i['name'], base=i['base'], description=i['description'], flash=i['flash'],
                    wic_file=i['wic_file'], uboot_name=i['uboot_name'], uboot_start=i['uboot_start'],
                    uboot_end=i['uboot_end'], kernel_name=i['kernel_name'], kernel_start=i['kernel_start'],
                    kernel_end=i['kernel_end'], fs_name=i['fs_name'], fs_start=i['fs_start'], fs_end=i['fs_end'])

            for p in i['packages']:
                MyImagePackage.objects.create(image=image, name=p['name'], description=p['description'], version=p['version'])