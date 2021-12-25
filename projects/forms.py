from sys import path
from typing_extensions import Required
from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import ExtraMarco, Project, MetaLayer, Build, MyConf, MyPackages, Tasks, LocalFile

class ProjectModelForm(forms.ModelForm):

    class Meta:

        model = Project
        fields = '__all__'

        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'project_path': forms.TextInput(attrs={'class': 'u-full-width'}),
            'project_version': forms.Select(attrs={'class': 'u-full-width'}),
        }

        labels = {
            'project_name': 'Project Name',
            'project_path': 'Project Path',
            'project_version': 'Yocto Version',
        }

class MetaModelForm(forms.ModelForm):

    class Meta:

        model = MetaLayer
        fields = ['url', 'name']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'u-full-width'}),
            'name': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'meta-xx'}),
        }

        labels = {
            'name': 'Name',
            'url': 'Url',
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
                'depends', 'description', 'local_files','src_url', 'src_rev', 'src_url_md5',
                'src_url_sha256', 'files_install_directory', 'building_directory',
                'inherit', 'language', 'donwload_method', 'initial_method', 'systemd_auto_enable',
                'systemd_service_name')
        
        not_required = ('license_default', 'license', 'lic_files_chksum','depends', 'description', 'local_files',
                'src_url', 'src_rev', 'src_url_md5','src_url_sha256', 'files_install_directory',
                'building_directory', 'inherit', 'initial_method', 'language', 'systemd_service_name', 'systemd_auto_enable')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder':'my-bbfile'}),
            'type': forms.Select(attrs={'class': 'u-full-width'}),
            'language': forms.Select(attrs={'class': 'u-full-width'}),
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
            'building_directory': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'The working folder which contain the files that need by bitbake tasks'}),
            'local_files': forms.TextInput(attrs={'class': 'u-full-width', 'placeholder': 'file://file1;file://file2...'}),
            'inherit': forms.TextInput(attrs={'class': 'u-full-width'}),
            'systemd_auto_enable': forms.Select(attrs={'class': 'u-full-width'}),
            'systemd_service_name': forms.TextInput(attrs={'class': 'u-full-width'})
        }

        labels = {
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
        fields = ['name', 'value', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-full-width'}),
            'value': forms.TextInput(attrs={'class': 'u-full-width'}), 
            'description': forms.TextInput(attrs={'class': 'u-full-width'}), 
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
    old = forms.CharField(max_length=3000, 
                    widget=forms.Textarea(attrs={'class': 'u-full-width', "style":"height: 300px;"}),
                    label='Old Content')
    new = forms.CharField(max_length=3000, 
                    widget=forms.Textarea(attrs={'class': 'u-full-width', "style":"height: 300px;"}),
                    label='New Content')

