from random import choice
from django import forms
from .models import *
from django.contrib.postgres.forms import SimpleArrayField

class ProjectModelForm(forms.ModelForm):

    class Meta:

        model = Project
        fields = ['project_name', 'project_version']

        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'project_version': forms.Select(attrs={'class': 'u-full-width'}),
        }

        labels = {
            'project_name': 'Project Name',
            'project_version': 'Yocto Version',
        }

class ProjectImportForm(forms.Form):

    name = forms.CharField(max_length=60, 
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}))
    url = forms.CharField(max_length=300,
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}))
                    
class MetaModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.not_required:
            self.fields[field].required = False

    class Meta:

        model = MetaLayer
        fields = ['url', 'name', 'remote_or_local', 'sub']

        not_required = ['url', 'sub']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'u-full-width'}),
            'name': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'meta-xx'}),
            'remote_or_local': forms.Select(attrs={'class': 'u-full-width'}),
            'sub': forms.TextInput(attrs={'class': 'u-full-width'}),
        }

        labels = {
            'name': 'Name',
            'url': 'Url',
            'remote_or_local': 'Remote or Local',
        }

class BuildModelForm(forms.ModelForm):

    class Meta:

        model = Build
        fields = ['target', 'command']

        widgets = {
            'target': forms.TextInput(attrs={'class': 'u-full-width'}),
            'command': forms.TextInput(attrs={'class': 'u-full-width'}),            
        }

        labels = {
            'target': 'Build Target',
            'command': 'Build Command',
        }

class MyConfModelForm(forms.ModelForm):

    class Meta:

        model = MyConf
        fields = ['name', 'value', 'strength']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'meta-xx'}),
            'value': forms.TextInput(attrs={'class': 'u-full-width'}),
            'strength': forms.Select(attrs={'class': 'u-full-width'}),       
        }

        labels = {
            'name': 'Marco Name ',
            'value': 'Marco Value',
            'strength': 'Value Strength'
        }

class MyPackagesModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.not_required:
            self.fields[field].required = False

    class Meta:

        model = MyPackages
        fields = ('name', 'type', 'version', 'license_default', 'license', 'lic_files_chksum',
                'depends', 'description', 'local_files','src_url', 'src_rev', 'src_url_md5', 'extra_oemake',
                'src_url_sha256', 'files_install_directory', 'building_directory', 'files_pn', 'go_proxy',
                'inherit', 'language', 'donwload_method', 'initial_method', 'systemd_auto_enable',
                'systemd_service_name', 'config_file_path', 'go_env', 'source_directory', 'catagory')
        
        not_required = ('license_default', 'license', 'lic_files_chksum','depends', 'description', 'local_files',
                'src_url', 'src_rev', 'src_url_md5','src_url_sha256', 'files_install_directory', 'go_proxy',
                'building_directory', 'inherit', 'initial_method', 'language', 'systemd_service_name', 'systemd_auto_enable', 
                'config_file_path', 'go_env', 'source_directory', 'catagory', 'files_pn', 'extra_oemake')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder':'my-bbfile'}),
            'type': forms.Select(attrs={'class': 'u-full-width'}),
            'language': forms.Select(attrs={'class': 'u-full-width'}),
            'catagory': forms.Select(attrs={'class': 'u-full-width'}),
            'donwload_method': forms.Select(attrs={'class': 'u-full-width'}),
            'initial_method': forms.Select(attrs={'class': 'u-full-width'}),            
            'license_default': forms.Select(attrs={'class': 'u-full-width'}),
            'version': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': '1.0.0'}),
            'license': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'MIT'}),
            'lic_files_chksum': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302'}),
            'depends': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'depend packages'}),
            'description': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'this is a xx software'}),
            'src_url': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'git://xxx.git;protocol=https;tag=v${PV}'}),
            'src_rev': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'when clone remote repo, you need to fill in'}),    
            'src_url_md5': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'When downloading remote files, you need to fill in'}),
            'src_url_sha256': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'When downloading remote files, you need to fill in'}),
            'files_install_directory': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'The folder in the filesystem that you wish to mount'}),
            'building_directory': forms.TextInput(attrs={'class': 'u-full-width'}),
            'local_files': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'file://file1;file://file2...'}),
            'inherit': forms.TextInput(attrs={'class': 'u-full-width'}),
            'systemd_auto_enable': forms.Select(attrs={'class': 'u-full-width'}),
            'systemd_service_name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'config_file_path': forms.TextInput(attrs={'class': 'u-full-width'}),
            'go_env': forms.TextInput(attrs={'class': 'u-full-width'}),
            'go_proxy': forms.TextInput(attrs={'class': 'u-full-width'}),
            'source_directory': forms.TextInput(attrs={'class': 'u-full-width'}),
            'extra_oemake': forms.TextInput(attrs={'class': 'u-full-width'}),
        }

        labels = {
            'depends': 'Depends (You can enter multiple dependencies, separated by spaces)',
            'src_rev': 'Src Revision',
            'src_url': 'Src Url',
            'src_url_md5': 'Src Url Md5',
            'src_url_sha256': 'Src Url Sha256',
            'local_files': 'Local Files',
            'license_default': 'Project Integrated License',
            'donwload_method': 'Download Method',
            'initial_method': 'Initial Method',
            'systemd_auto_enable': 'Service Auto Enable',
            'systemd_service_name': 'Service File Name',
            'building_directory': 'Build Directory ($B)',
            'source_directory': 'Source Directory ($S)',
            'go_env': 'Extra Golang Env Variable (Seperate by comma)',
            'extra_oemake': 'Extra Oemake ($EXTRA_OEMAKE, Seperate by comma)',
            'go_proxy': 'GOPROXY'
        }

class TaskModelForm(forms.ModelForm):

    class Meta:

        model = Tasks
        fields = ['type', 'subtype', 'op', 'description']

        widgets = {
            'op': forms.TextInput(attrs={'class': 'u-full-width'}),
            'description': forms.TextInput(attrs={'class': 'u-full-width'}),    
            'type': forms.Select(attrs={'class': 'u-full-width'}),
            'subtype': forms.Select(attrs={'class': 'u-full-width'}),       
        }

class ExtraMarcoModelForm(forms.ModelForm):

    class Meta:

        model = ExtraMarco
        fields = ['name', 'value', 'description', 'strength']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'value': forms.TextInput(attrs={'class': 'u-full-width'}), 
            'description': forms.TextInput(attrs={'class': 'u-full-width'}), 
            'strength': forms.Select(attrs={'class': 'u-full-width'})
        }

class LocalFileModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.not_required:
            self.fields[field].required = False

    class Meta:

        model = LocalFile
        fields = ['name', 'path', 'content']

        not_required = ('path', 'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'path': forms.TextInput(attrs={'class': 'u-full-width'}),
            'content': forms.Textarea(attrs={'class': 'u-full-width', "style":"height: 600px;"}),
        }

class GeneratePatchFileForm(forms.Form):
    name = forms.CharField(max_length=60, 
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}))
    path = forms.CharField(max_length=300,
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}),
                    label='File Path in Original Project')
    old = forms.CharField(max_length=60000, 
                    widget=forms.Textarea(attrs={'class': 'u-full-width', "style":"height: 300px;"}),
                    label='Old Content')
    new = forms.CharField(max_length=60000, 
                    widget=forms.Textarea(attrs={'class': 'u-full-width', "style":"height: 300px;"}),
                    label='New Content')

class MyMachineModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.not_required:
            self.fields[field].required = False
                    

    class Meta:

        model = MyMachine
        fields = ['name', 'description', 'base', 'uboot', 'kernel', 'flash', 
                'filesystem', 'initial_method', 'jffs2_eraseblock', 'mkubifs_args',
                'ubinize_args', 'mxsboot_nand_args', 'machine_include', 'distro_include',
                'kernel_dts', 'uboot_defconfig', 'kernel_defconfig', 'machineoverrides',
                'distro_version']

        not_required = ('name', 'uboot', 'kernel', 'flash', 'filesystem', 'jffs2_eraseblock', 
                 'mkubifs_args', 'ubinize_args', 'mxsboot_nand_args', 'machine_include',
                'distro_include', 'kernel_dts', 'uboot_defconfig', 'kernel_defconfig', 
                'machineoverrides')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'description': forms.TextInput(attrs={'class': 'u-full-width'}),
            'base': forms.Select(attrs={'class': 'u-full-width'}),
            'uboot': forms.TextInput(attrs={'class': 'u-full-width'}),
            'kernel': forms.TextInput(attrs={'class': 'u-full-width'}),
            'flash': forms.Select(attrs={'class': 'u-full-width'}),
            'filesystem': forms.TextInput(attrs={'class': 'u-full-width'}),
            'initial_method': forms.Select(attrs={'class': 'u-full-width'}),
            'jffs2_eraseblock': forms.TextInput(attrs={'class': 'u-full-width'}),
            'mkubifs_args': forms.TextInput(attrs={'class': 'u-full-width'}),
            'ubinize_args': forms.TextInput(attrs={'class': 'u-full-width'}),
            'mxsboot_nand_args': forms.TextInput(attrs={'class': 'u-full-width'}),
            'machine_include': forms.TextInput(attrs={'class': 'u-full-width'}),
            'distro_include': forms.TextInput(attrs={'class': 'u-full-width'}),
            'kernel_dts': forms.TextInput(attrs={'class': 'u-full-width'}),
            'uboot_defconfig': forms.TextInput(attrs={'class': 'u-full-width'}),
            'kernel_defconfig': forms.TextInput(attrs={'class': 'u-full-width'}),
            'machineoverrides': forms.TextInput(attrs={'class': 'u-full-width'}),
            'distro_version': forms.TextInput(attrs={'class': 'u-full-width'}),
        }

        labels = {
            'base': 'Chip & Board',

            'initial_method': 'Systemd or System-V',
            'donwload_method': 'Download Method',
            'machine_include': 'Machine File Include',
            'distro_include': 'Distro File Include',
            'kernel_dts': 'Kernel DeviceTree',
            'machineoverrides': 'MACHINEOVERRIDES',
            'distro_version': 'Version',
        }


class ExtraMachineMarcoModelForm(forms.ModelForm):

    class Meta:

        model = MachineExtraMarco
        fields = ['name', 'value', 'description', 'strength']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'value': forms.TextInput(attrs={'class': 'u-full-width'}), 
            'description': forms.TextInput(attrs={'class': 'u-full-width'}), 
            'strength': forms.Select(attrs={'class': 'u-full-width'}),            
        }


class MyImageModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.not_required:
            self.fields[field].required = False
    
    class Meta:

        model = MyImage
        fields = ['name', 'base', 'flash', 'description', 'wic_file', 'uboot_name',
                'uboot_start', 'uboot_end', 'kernel_name', 'kernel_start', 'kernel_end',
                'fs_name', 'fs_start', 'fs_end', 'packages']

        not_required = ['wic_file' ,'uboot_name', 'uboot_start', 'uboot_end',
                    'kernel_name', 'kernel_start', 'kernel_end', 'fs_name', 
                    'fs_start', 'fs_end', 'packages']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'description': forms.TextInput(attrs={'class': 'u-full-width'}),
            'base': forms.Select(attrs={'class': 'u-full-width'}),
            'flash': forms.Select(attrs={'class': 'u-full-width'}),
            'wic_file': forms.TextInput(attrs={'class': 'u-full-width'}),
            'uboot_name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'uboot_start': forms.TextInput(attrs={'class': 'u-full-width'}),
            'uboot_end': forms.TextInput(attrs={'class': 'u-full-width'}),
            'kernel_name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'kernel_start': forms.TextInput(attrs={'class': 'u-full-width'}),
            'kernel_end': forms.TextInput(attrs={'class': 'u-full-width'}),
            'fs_name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'fs_start': forms.TextInput(attrs={'class': 'u-full-width'}),
            'fs_end': forms.TextInput(attrs={'class': 'u-full-width'}),
            'packages': forms.Textarea(attrs={'class': 'u-full-width', "style":"height: 200px;"}),
        }

        labels = {
            'packages': 'Import packages (Seperate by comma)'
        }

class MyImagePackageModelForm(forms.ModelForm):

    class Meta:

        model = MyImagePackage
        fields = ['name', 'description', 'version']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'description': forms.TextInput(attrs={'class': 'u-full-width'}),
            'version': forms.TextInput(attrs={'class': 'u-full-width'}),
        }

class MyConfForm(forms.Form):
    machine = forms.CharField(max_length=60, 
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}))
    distro = forms.CharField(max_length=300,
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}))
    parallel_make = forms.CharField(max_length=100,
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}),
                    label='Make Parallel Number')
    max_parallel_threads = forms.CharField(max_length=100, 
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}),
                    label='Max Parallel Tasks Number')

class InstallTaskForm(forms.Form):
    name = forms.CharField(max_length=60, 
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}))
    install_path = forms.CharField(max_length=300,
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}))
    source_path = forms.CharField(max_length=300,
                    widget=forms.TextInput(attrs={'class': 'u-full-width'}))
    permission = forms.CharField(max_length=100,
                    widget=forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'excute permission'}))
    is_directory = forms.ChoiceField(widget=forms.Select(attrs={'class': 'u-full-width'}),
                    label='Is Directory?', choices=[('no', 'No'), ('yes', 'Yes')])
    type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'u-full-width'}),
                    label='Install Type', choices=[('none', 'None'), ('append', 'Append'), ('prepend', 'Prepend')])


class MyImageExtraMarcoModelForm(forms.ModelForm):

    class Meta:

        model = MyImageExtraMarco
        fields = ['name', 'value', 'description', 'strength']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'value': forms.TextInput(attrs={'class': 'u-full-width'}), 
            'description': forms.TextInput(attrs={'class': 'u-full-width'}), 
            'strength': forms.Select(attrs={'class': 'u-full-width'})
        }