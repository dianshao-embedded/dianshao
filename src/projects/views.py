from celery import Task
from django.shortcuts import redirect, render
from django.template import context
from django.urls import reverse
from .models import *
from .forms import *
from .tasks import *
from os import path
# Create your views here.

def project(request):
    projects =  Project.objects.all()
    form = ProjectModelForm()
    form_import = ProjectImportForm()

    if request.method == 'POST':
        form = ProjectModelForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.project_path = '/app/yocto'
            project.save()
            result = shell_cmd_task.delay("mkdir %s/%s" % (project.project_path, project.project_name), project.project_path)
            while 1:
                if (result._get_task_meta())["status"] == 'FAILURE':
                    raise Exception('shell command task error')
                elif (result._get_task_meta())["status"] == 'SUCCESS':
                    break

        return redirect(reverse('projects:initial', args=(project.id,)))

    context = {
        'projects': projects,
        'form': form,
        'form_import': form_import,
    }

    return render(request, 'projects/projects.html', context)

def project_initial(request, project_id):
    project = Project.objects.get(id=project_id)
    result = project_initial_task.delay(project.id, project.project_path, 
                                        project.project_version, project.project_name)
    return render(request, 'projects/project_initial.html', 
                context={'task_id': result.task_id, 'project_id': project_id})

def project_import(request):
    if request.method == 'POST':
        form = ProjectImportForm(request.POST)
        if form.is_valid():
            result = project_import_task.delay('/app/yocto',
                                            form.cleaned_data['name'],
                                            form.cleaned_data['url'])
                                        
            return render(request, 'projects/project_import.html', context={'task_id': result.task_id})


def project_delete(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        result = shell_cmd_task.delay('rm -rf %s' % 
                    (path.join(project.project_path, project.project_name)), project.project_path)
        while 1:
            if (result._get_task_meta())["status"] == 'FAILURE':
                raise Exception('shell command task error')
            elif (result._get_task_meta())["status"] == 'SUCCESS':
                break

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

def project_export(request, project_id):
    result = project_export_task.delay(project_id)
    return render(request, 'projects/project_export.html', context={'task_id': result.task_id})
    

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

def mypackages(request, project_id):
    mypackages = MyPackages.objects.filter(project__id=project_id)

    context = {
        'project_id': project_id,
        'mypackages': mypackages,
    }

    return render(request, 'projects/mypackages.html', context)

def myimages(request, project_id):
    myimages = MyImage.objects.filter(project__id=project_id)

    context = {
        'project_id': project_id,
        'myimages': myimages,
    }

    return render(request, 'projects/myimages.html', context)

def mypackage_create(request, project_id):
    form = MyPackagesModelForm()
    if request.method == 'POST':
        form = MyPackagesModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.project = Project.objects.get(id=project_id)
            if form_obj.language == 'Golang':
                form_obj.depends = 'go-native'
            form_obj.save()
        
        return redirect(reverse('projects:mypackages', args=(project_id,)))
            
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

def install_task_create(request, project_id, mypackage_id):
    form = InstallTaskForm()
    context = {
        'form': form,
        'project_id': project_id,
    }

    if request.method == 'POST':
        form = InstallTaskForm(request.POST)
        if form.is_valid():
            package = MyPackages.objects.get(id=mypackage_id)
            type = 'do_install'
            subtype = form.cleaned_data['type']
            op1 = ("install -d %s" % form.cleaned_data['install_path'])
            desc1 = ("enter %s" % form.cleaned_data['install_path'])
            op2 = ("install -m %s %s/%s %s" % (form.cleaned_data['permission'], 
                    form.cleaned_data['source_path'], form.cleaned_data['name'], 
                    form.cleaned_data['install_path']))
            desc2 = ("copy file %s to %s" % (form.cleaned_data['name'], form.cleaned_data['install_path']))

            Tasks.objects.create(package=package, type=type, subtype=subtype, op=op1, description=desc1)
            Tasks.objects.create(package=package, type=type, subtype=subtype, op=op2, description=desc2)
        return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id)))
            
    return render(request, 'projects/install_task_create.html', context)

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
            result = bbfile_localfile_create_task.delay(mypackage.name, mypackage.version, mypackage.type,
                            path.join(project.project_path, project.project_name),
                            form.cleaned_data['name'], form.cleaned_data['content'])

            while 1:
                if (result._get_task_meta())["status"] == 'FAILURE':
                    raise Exception('shell command task error')
                elif (result._get_task_meta())["status"] == 'SUCCESS':
                    break
            
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
            result = bbfile_localfile_create_task.delay(mypackage.name, mypackage.version, mypackage.type,
                            path.join(project.project_path, project.project_name),
                            form.cleaned_data['path'], form.cleaned_data['name'])

            while 1:
                if (result._get_task_meta())["status"] == 'FAILURE':
                    raise Exception('shell command task error')
                elif (result._get_task_meta())["status"] == 'SUCCESS':
                    break

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
            result = patch_generator_task.delay(form.cleaned_data['name'], form.cleaned_data['path'],
                                path.join(project.project_path, project.project_name),
                                mypackage.name, mypackage.version, mypackage.type,
                                form.cleaned_data['old'], form.cleaned_data['new'])

            while 1:
                if (result._get_task_meta())["status"] == 'FAILURE':
                    raise Exception('shell command task error')
                elif (result._get_task_meta())["status"] == 'SUCCESS':
                    break

            LocalFile.objects.create(package=mypackage, name=form.cleaned_data['name'] + '.patch',
                                    type = 'patch')                    
            return redirect(reverse('projects:mypackage_detail', args=(project_id, mypackage_id)))                    

    return render(request, 'projects/generata_patch_file.html', context)

def mypackage_bbfile(request, project_id, mypackage_id):
    project = Project.objects.get(id=project_id)
    mypackage = MyPackages.objects.get(id=mypackage_id)
    result = bbfile_task_create.delay(mypackage.name, mypackage.version, mypackage.type,
                        path.join(project.project_path, project.project_name),
                        mypackage_id)

    while 1:
        if (result._get_task_meta())["status"] == 'FAILURE':
            raise Exception('shell command task error')
        elif (result._get_task_meta())["status"] == 'SUCCESS':
            break

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


def mymachine(request, project_id):
    project = Project.objects.get(id=project_id)
    mymachine = MyMachine.objects.get(project__id=project_id)
    form = MyMachineModelForm(instance=mymachine)

    extraMarcos = MachineExtraMarco.objects.filter(machine__id = mymachine.id).order_by('id')

    context={
        'form': form,
        'extraMarcos': extraMarcos,
        'project_id': project_id,
        'mymachine_id': mymachine.id,
    }

    if request.method == 'POST':
        form = MyMachineModelForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.project = project
            form_obj.name = mymachine.name
            form_obj.id = mymachine.id
            form_obj.save()
            
        return redirect(reverse('projects:mymachine', args=(project_id,)))


    return render(request, 'projects/mymachine.html', context)

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
        
        return redirect(reverse('projects:mymachine', args=(project_id,)))
            
    return render(request, 'projects/extra_machine_marco_create.html', context)

def mymachine_file(request, project_id, mymachine_id):
    project = Project.objects.get(id=project_id)
    result = machinefile_create_task.delay(mymachine_id)
    while 1:
        if (result._get_task_meta())["status"] == 'FAILURE':
            raise Exception('shell command task error')
        elif (result._get_task_meta())["status"] == 'SUCCESS':
            break
    return redirect(reverse('projects:mymachine', args=(project_id,))) 


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
        
        return redirect(reverse('projects:myimages', args=(project_id,)))

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
            if form_obj.language == 'Golang':
                form_obj.depends = 'go-native'
            if form_obj.donwload_method == 'git':
                form_obj.building_directory = "$(WORKDIR)/git"
            form_obj.save()
        
        return redirect(reverse('projects:myimage_detail', args=(project_id, myimage_id)))
            
    return render(request, 'projects/package_import.html', context)

def myimage_file(request, project_id, myimage_id):
    result = imagefile_create_task.delay(myimage_id)
    while 1:
        if (result._get_task_meta())["status"] == 'FAILURE':
            raise Exception('shell command task error')
        elif (result._get_task_meta())["status"] == 'SUCCESS':
            break

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
            result = config_set_task.delay(project_id,
                                form.cleaned_data['machine'],
                                form.cleaned_data['distro'],
                                form.cleaned_data['parallel_make'],
                                form.cleaned_data['max_parallel_threads'])
            while 1:
                if (result._get_task_meta())["status"] == 'FAILURE':
                    raise Exception('shell command task error')
                elif (result._get_task_meta())["status"] == 'SUCCESS':
                    break

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