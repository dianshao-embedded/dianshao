from typing import ContextManager
from django.shortcuts import redirect, render
from django.urls import reverse
from tools.shell import shell_cmd
from tools.bbfile import DianshaoBBFile, DianshaoConfFile, DianshaoImageFile, DianshaoMachineFile
from tools.patch import patch_generator
from .models import *
from .forms import *
from .tasks import project_initial_task, meta_clone_task
from .tasks import bitbake_progress
from os import path
# Create your views here.

def project(request):
    projects =  Project.objects.all()
    form = ProjectModelForm()

    if request.method == 'POST':
        form = ProjectModelForm(request.POST)
        if form.is_valid():
            project = form.save()
            #TODO: 创建基础项目并显示进度
            ret, error = shell_cmd("mkdir %s/%s" % (project.project_path, project.project_name), project.project_path)
            if error:
                raise Exception(ret)
        return redirect(reverse('projects:initial', args=(project.id,)))

    context = {
        'projects': projects,
        'form': form,
    }

    return render(request, 'projects/projects.html', context)

def project_initial(request, project_id):
    project = Project.objects.get(id=project_id)
    result = project_initial_task.delay(project.id, project.project_path, 
                                        project.project_version, project.project_name)
    return render(request, 'projects/project_initial.html', 
                context={'task_id': result.task_id, 'project_id': project_id})

def project_delete(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        ret, err = shell_cmd('rm -rf %s' % 
                    (path.join(project.project_path, project.project_name)), project.project_path)
        if err:
            raise Exception(ret)

        project.delete()

    return redirect('/projects/')


def metas(request, project_id):
    metas = MetaLayer.objects.filter(project__id=project_id)
    return render(request, 'projects/metas.html',context={'metas': metas, 'project_id': project_id})

def meta_create(request, project_id):
    # TODO: add meta-layer to config files
    project = Project.objects.get(id=project_id)
    form = MetaModelForm()

    if request.method == 'POST':
        form = MetaModelForm(request.POST)
        if form.is_valid():
            result = meta_clone_task.delay(form.cleaned_data['name'],
                                            form.cleaned_data['url'],
                                            form.cleaned_data['remote_or_local'],
                                            form.cleaned_data['sub'],
                                            project.id)

            return render(request, 'projects/meta_create.html', 
                    context={'form': form, 'task_id': result.task_id, 'project_id': project_id})

        else:
            return render(request, 'projects/meta_create.html', context={'form': form})

    else:
        return render(request, 'projects/meta_create.html', context={'form': form})


def bitbake(request, project_id):
    # TODO: 决定还是不开发bitbake自由编译权限，只提供myMeta 菜单编译， uboot 编译， 内核编译和全项目编译
    project = Project.objects.get(id=project_id)
    form = BuildModelForm()

    if request.method == 'POST':
        form = BuildModelForm(request.POST)
        if form.is_valid():
            result = bitbake_progress.delay(project.project_path, 
                                            project.project_name, 
                                            form.cleaned_data['target'],
                                            form.cleaned_data['command'])
                                
            return render(request, 'projects/bitbake_cmd.html', context={'form': form, 'task_id': result.task_id, 'project_id': project_id})
        else:
            return render(request, 'projects/bitbake_cmd.html', context={'form': form})    

    else:
        return render(request, 'projects/bitbake_cmd.html', context={'form': form})


def mymeta(request, project_id):
    # TODO: mymeta add mymachine and myimage
    mypackages = MyPackages.objects.filter(project__id=project_id)
    mymachines = MyMachine.objects.filter(project__id=project_id)
    myimages = MyImage.objects.filter(project__id=project_id)

    context = {
        'project_id': project_id,
        'mypackages': mypackages,
        'mymachines': mymachines,
        'myimages': myimages,
    }

    return render(request, 'projects/mymeta.html', context)

def mypackage_create(request, project_id):
    form = MyPackagesModelForm()
    if request.method == 'POST':
        form = MyPackagesModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.project = Project.objects.get(id=project_id)
            form_obj.save()
        
        return redirect(reverse('projects:mymeta', args=(project_id,)))
            
    return render(request, 'projects/mypackage_create.html', context={'form': form, 'project_id': project_id})

def mypackage_detail(request, project_id, mypackage_id):
    project = Project.objects.get(id=project_id)
    mypackage = MyPackages.objects.get(id=mypackage_id)
    form = MyPackagesModelForm(instance=mypackage)

    tasks = Tasks.objects.filter(package__id = mypackage_id).order_by('id')
    localfiles = LocalFile.objects.filter(package__id = mypackage_id).order_by('id')
    extraMarcos = ExtraMarco.objects.filter(package__id = mypackage_id).order_by('id')

    context={
        'form': form,
        'tasks': tasks,
        'localfiles': localfiles,
        'extraMarcos': extraMarcos,
        'project_id': project_id,
        'mypackage_id': mypackage_id,
    }

    if request.method == 'POST':
        form = MyPackagesModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.project = project
            form_obj.id = mypackage_id
            form_obj.save()
            
        return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id)))


    return render(request, 'projects/mypackage_detail.html', context)

def task_create(request, project_id, mypackage_id):
    form = TaskModelForm()
    context = {
        'form': form,
        'project_id': project_id,
    }

    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.package = MyPackages.objects.get(id=mypackage_id)
            form_obj.save()
        
        return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id)))
            
    return render(request, 'projects/task_create.html', context)

def extra_marco_create(request, project_id, mypackage_id):
    form = ExtraMarcoModelForm()
    context = {
        'form': form,
        'project_id': project_id,
    }

    if request.method == 'POST':
        form = ExtraMarcoModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.package = MyPackages.objects.get(id=mypackage_id)
            form_obj.save()
        
        return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id)))
            
    return render(request, 'projects/extra_marco_create.html', context)

def file_create(request, project_id, mypackage_id):
    # TODO: add auto install path target
    form = LocalFileModelForm()
    mypackage = MyPackages.objects.get(id=mypackage_id)
    project = Project.objects.get(id=project_id)

    context = {
        'form': form,
        'project_id': project_id,
        'mypackage_id': mypackage_id,
    }

    if request.method == 'POST':
        # TODO: Do not SAVE file content!
        form = LocalFileModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            bbfile = DianshaoBBFile(mypackage.name, mypackage.version, mypackage.type)
            bbfile.create_folder(path.join(project.project_path, project.project_name))
            bbfile.create_local_file(form.cleaned_data['name'], form.cleaned_data['content'])
            form_obj.package = mypackage
            form_obj.type = 'New File'
            form_obj.content = 'Do not SAVE file content!'
            form_obj.save()
        return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id)))

    return render(request, 'projects/create_file.html', context)


def file_import(request, project_id, mypackage_id):
    form = LocalFileModelForm()
    mypackage = MyPackages.objects.get(id=mypackage_id)
    project = Project.objects.get(id=project_id)

    context = {
        'form': form,
        'project_id': project_id,
        'mypackage_id': mypackage_id,
    }

    if request.method == 'POST':
        form = LocalFileModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            bbfile = DianshaoBBFile(mypackage.name, mypackage.version, mypackage.type)
            bbfile.create_folder(path.join(project.project_path, project.project_name))
            bbfile.import_local_file(form.cleaned_data['path'], form.cleaned_data['name'])
            form_obj.package = mypackage
            form_obj.type = 'Import File'
            form_obj.save()
        return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id)))

    return render(request, 'projects/import_file.html', context)

def file_generate_patch(request, project_id, mypackage_id):
    form = GeneratePatchFileForm()
    mypackage = MyPackages.objects.get(id=mypackage_id)
    project = Project.objects.get(id=project_id)

    context = {
        'form': form,
        'project_id': project_id,
        'mypackage_id': mypackage_id,
    }

    if request.method == 'POST':
        form = GeneratePatchFileForm(request.POST)
        if form.is_valid():
            patch_generator(form.cleaned_data['name'], form.cleaned_data['path'],
                                path.join(project.project_path, project.project_name),
                                mypackage.name, mypackage.version, mypackage.type,
                                form.cleaned_data['old'], form.cleaned_data['new'])

            LocalFile.objects.create(package=mypackage, name=form.cleaned_data['name'] + '.patch',
                                    type = 'patch')                    
            return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id)))                    

    return render(request, 'projects/generata_patch_file.html', context)

def mypackage_bbfile(request, project_id, mypackage_id):
    project = Project.objects.get(id=project_id)
    mypackage = MyPackages.objects.get(id=mypackage_id)
    bbfile = DianshaoBBFile(mypackage.name, mypackage.version, mypackage.type)
    bbfile.create_folder(path.join(project.project_path, project.project_name))
    bbfile.create_bbfile(mypackage_id)
    return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id))) 

def mypackage_bitbake(request, project_id, mypackage_id):
    project = Project.objects.get(id=project_id)
    mypackage = MyPackages.objects.get(id=mypackage_id)

    result = bitbake_progress.delay(project.project_path, 
                                    project.project_name, 
                                    mypackage.name, 'build')

    context={
        'task_id': result.task_id,
        'project_id': project_id,
        'mypackage_id': mypackage_id,
        'package_name': mypackage.name,
    }
                                
    return render(request, 'projects/mypackage_bitbake.html', context)


def mymachine_create(request, project_id):
    form = MyMachineModelForm()
    if request.method == 'POST':
        form = MyMachineModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.project = Project.objects.get(id=project_id)
            if form_obj.flash == 'Spi-Nor':
                form_obj.filesystem = 'jffs2'
            elif form_obj.flash == 'Rawnand':
                form_obj.filesystem = 'ubifs'
            else:
                form_obj.filesystem = 'ext4'
            form_obj.save()
        
        return redirect(reverse('projects:mymeta', args=(project_id,)))
        
    return render(request, 'projects/mymachine_create.html', 
                context={'form': form, 'project_id': project_id})


def mymachine_detail(request, project_id, mymachine_id):
    project = Project.objects.get(id=project_id)
    mymachine = MyMachine.objects.get(id=mymachine_id)
    form = MyMachineModelForm(instance=mymachine)

    extraMarcos = MachineExtraMarco.objects.filter(machine__id = mymachine_id).order_by('id')

    context={
        'form': form,
        'extraMarcos': extraMarcos,
        'project_id': project_id,
        'mymachine_id': mymachine_id,
    }

    if request.method == 'POST':
        form = MyMachineModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.project = project
            form_obj.id = mymachine_id
            form_obj.save()
            
        return redirect(reverse('projects:mymachine_detail', args=(project_id, mymachine_id)))


    return render(request, 'projects/mymachine_detail.html', context)

def extra_machine_marco_create(request, project_id, mymachine_id):
    form = ExtraMachineMarcoModelForm()
    context = {
        'form': form,
        'project_id': project_id,
    }

    if request.method == 'POST':
        form = ExtraMachineMarcoModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.machine = MyMachine.objects.get(id=mymachine_id)
            form_obj.save()
        
        return redirect(reverse('projects:mymachine_detail', args=(project_id, mymachine_id)))
            
    return render(request, 'projects/extra_machine_marco_create.html', context)

def mymachine_file(request, project_id, mymachine_id):
    project = Project.objects.get(id=project_id)
    machine_file = DianshaoMachineFile(mymachine_id)
    machine_file.create_machine_file()
    machine_file.create_distro_file()
    #machine_file.set_config_file()
    return redirect(reverse('projects:mymachine_detail', args=(project_id, mymachine_id))) 


def myimage_create(request, project_id):
    form = MyImageModelForm()
    context = {
        'form': form,
        'project_id': project_id
    }
    if request.method == 'POST':
        form = MyImageModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.project = Project.objects.get(id=project_id)
            form_obj.save()
        
        return redirect(reverse('projects:mymeta', args=(project_id,)))

    return render(request, 'projects/myimage_create.html', context)

def myimage_detail(request, project_id, myimage_id):
    project = Project.objects.get(id=project_id)
    myimage = MyImage.objects.get(id=myimage_id)
    form = MyImageModelForm(instance=myimage)

    packages = MyImagePackage.objects.filter(image__id = myimage_id).order_by('id')
    context={
        'form': form,
        'packages': packages,
        'project_id': project_id,
        'myimage_id': myimage_id,
    }

    if request.method == 'POST':
        form = MyImageModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.project = project
            form_obj.id = myimage_id
            form_obj.save()
            
        return redirect(reverse('projects:myimage_detail', args=(project_id, myimage_id)))

    return render(request, 'projects/myimage_detail.html', context)

def myimagepackage_create(request, project_id, myimage_id):
    form = MyImagePackageModelForm()
    context = {
        'form': form,
        'project_id': project_id,
    }

    if request.method == 'POST':
        form = MyImagePackageModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.image = MyImage.objects.get(id=myimage_id)
            form_obj.save()
        
        return redirect(reverse('projects:myimage_detail', args=(project_id, myimage_id)))
            
    return render(request, 'projects/package_import.html', context)

def myimage_file(request, project_id, myimage_id):
    imagefile = DianshaoImageFile(myimage_id)
    imagefile.create_image_file()
    project = Project.objects.get(id=project_id)
    myimage = MyImage.objects.get(id=myimage_id)

    result = bitbake_progress.delay(project.project_path, 
                                    project.project_name, 
                                    myimage.name, 'build')

    context={
        'task_id': result.task_id,
        'project_id': project_id,
        'myimage_id': myimage_id,
        'image_name': myimage.name,
    }
                                
    return render(request, 'projects/image_bitbake.html', context)

def myconf_update(request, project_id):
    form = MyConfForm()
    context = {
        'form': form,
        'project_id': project_id,
    }

    if request.method == 'POST':
        form = MyConfForm(request.POST)
        if form.is_valid():
            conf = DianshaoConfFile(project_id)
            conf.set_config_file(form.cleaned_data['machine'],
                                form.cleaned_data['distro'],
                                form.cleaned_data['parallel_make'],
                                form.cleaned_data['max_parallel_threads'])

        return redirect(reverse('projects:mymeta', args=(project_id,)))    
    
    return render(request, 'projects/myconf_update.html', context)

"""
def uboot_bitbake(request, project_id, myimage_id):
    project = Project.objects.get(id=project_id)
    myimage = MyImage.objects.get(id=myimage_id)
    machine = MyMachine.objects.get(name = myimage.machine)

    result = bitbake_progress.delay(project.project_path, 
                                    project.project_name, 
                                    machine.uboot, 'build')

    context={
        'task_id': result.task_id,
        'project_id': project_id,
        'myimage_id': myimage_id,
    }
                                
    return render(request, 'projects/uboot_bitbake.html', context)


def kernel_bitbake(request, project_id, myimage_id):
    project = Project.objects.get(id=project_id)
    myimage = MyImage.objects.get(id=myimage_id)
    machine = MyMachine.objects.get(name = myimage.machine)

    result = bitbake_progress.delay(project.project_path, 
                                    project.project_name, 
                                    machine.kernel, 'build')

    context={
        'task_id': result.task_id,
        'project_id': project_id,
        'myimage_id': myimage_id,
    }
                                
    return render(request, 'projects/kernel_bitbake.html', context)

def image_bitbake(request, project_id, myimage_id):
    project = Project.objects.get(id=project_id)
    myimage = MyImage.objects.get(id=myimage_id)

    result = bitbake_progress.delay(project.project_path, 
                                    project.project_name, 
                                    myimage.name, 'build')

    context={
        'task_id': result.task_id,
        'project_id': project_id,
        'myimage_id': myimage_id,
        'image_name': myimage.name,
    }
                                
    return render(request, 'projects/image_bitbake.html', context)
"""