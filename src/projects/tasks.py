from datetime import datetime
import os
import socket
import json
from sqlite3 import Timestamp
from celery import shared_task
from progressui.backend import ProgressSend
from git.repo.base import Repo
from tools import shell, git, bbcommand, patch, bbfile
from tools import migration
from tools.migration import Migration
from .models import MetaLayer, MyMachine, MyPackages, Project

# TODO：后续提高稳定性，无论如何误操作可自恢复
@shared_task(bind=True)
def project_initial_task(self, project_id, project_path, project_version, project_name):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', 8866))
    progress_send = ProgressSend(self)
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'project_template')
    target_path = os.path.join(project_path, project_name)
    r, err = shell.shell_cmd('cp -rp %s/. %s' % (template_path, target_path), os.curdir)
    if err == True:
        raise Exception("project template build error: %s" % (r))

    project=Project.objects.get(id=project_id)
    MyMachine.objects.create(project=project, name='dianshao', base='none', initial_method='Systemd', flash='SDCard', 
                    distro_version='1.0.0', description='my machine generate by dianshao', 
                    machine_include='{}', distro_include='{}')

    # TODO: 根据项目名自动生成 distro, image, machine, bblayer, conf.sample 等文件
    Repo.init(target_path)
    progress_send.send_progress(percentage='25', description='Add Bitbake Submodule')

    if project_version == 'HARDKNOTT':
        yocto_version = 'hardknott'
        bitbake_version = '1.50'
    elif project_version == 'GATESGARTH':
        yocto_version = 'gatesgarth'
        bitbake_version = '1.48'
    elif project_version == 'DUNFELL':
        yocto_version = 'dunfell'
        bitbake_version = '1.46'
    elif project_version == 'ZEUS':
        yocto_version = 'zeus'
        bitbake_version = '1.44'

    # TODO: 任务失败恢复重新开始
    submodule = git.git_submodule(target_path, 'bitbake',
                    'https://github.com/openembedded/bitbake.git',
                    bitbake_version)
    submodule.start()

    path = os.path.join(project_path, project_name, 'bitbake')
    i = 0
    while(os.path.exists(path) == False and i < 3):
        while submodule.is_alive():
            try:
                server.settimeout(5)
                byte, addr = server.recvfrom(1024)
            except:
                continue
            gitMessage = json.loads(byte.decode('ascii'))
            sub = [{'percentage': int(gitMessage['cur_count']*100/gitMessage['max_count']), 'description': gitMessage['message']}]
            progress_send.send_progress(percentage='25',subProgress=sub, description='Add Bitbake Submodule')

        if os.path.exists(path):
            break
        else:
            i += 1

    if i == 3:
        raise Exception('git clone error')

    bitbake_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bitbake')
    r, err = shell.shell_cmd(command=('cp -r %s %s' % (bitbake_path, target_path)), cwd = target_path)
    if err == True:
        server.close()
        raise Exception("project template build error: %s" % (r))

    progress_send.send_progress(percentage='50', description='Add Openembedded-Core Submodule')

    submodule = git.git_submodule(target_path, 'openembedded-core',
                    'https://github.com/openembedded/openembedded-core.git',
                    yocto_version)
    submodule.start()
    
    path = os.path.join(project_path, project_name, 'openembedded-core')
    i = 0
    while(os.path.exists(path) == False and i < 3):
        while submodule.is_alive():
            try:
                server.settimeout(5)
                byte, addr = server.recvfrom(1024)
            except:
                continue
            gitMessage = json.loads(byte.decode('ascii'))
            sub = [{'percentage': int(gitMessage['cur_count']*100/gitMessage['max_count']), 'description': gitMessage['message']}]
            progress_send.send_progress(percentage='50', subProgress=sub, description='Add Openembedded-Core Submodule')
        
        if os.path.exists(path):
            break
        else:
            i += 1

    if i == 3:
        raise Exception('git clone error')

    project = Project.objects.get(id=project_id)
    MetaLayer.objects.create(project=project, 
                            name='openembedded-core', 
                            url='https://github.com/openembedded/openembedded-core.git',
                            remote_or_local = 'remote')
    
    progress_send.send_progress(percentage='75', description='Add Meta-Yocto Submodule')

    submodule = git.git_submodule(target_path, 'meta-yocto',
                    'https://git.yoctoproject.org/meta-yocto.git',
                    yocto_version)
    submodule.start()

    path = os.path.join(project_path, project_name, 'meta-yocto')
    i = 0
    while(os.path.exists(path) == False and i < 3):    

        while submodule.is_alive():
            try:
                server.settimeout(5)
                byte, addr = server.recvfrom(1024)
            except:
                continue
            gitMessage = json.loads(byte.decode('ascii'))
            sub = [{'percentage': int(gitMessage['cur_count']*100/gitMessage['max_count']), 'description': gitMessage['message']}]
            progress_send.send_progress(percentage='75', subProgress=sub, description='Add Meta-Yocto Submodule')               

        if os.path.exists(path):
            break
        else:
            i += 1

    if i == 3:
        raise Exception('git clone error')

    MetaLayer.objects.create(project=project,
                            name='meta-yocto', 
                            url='https://git.yoctoproject.org/meta-yocto.git',
                            remote_or_local = 'remote',
                            sub = 'meta-poky')

    MetaLayer.objects.create(project=project,
                            name='meta-yocto', 
                            url='https://git.yoctoproject.org/meta-yocto.git',
                            remote_or_local = 'remote',
                            sub = 'meta-yocto-bsp')                          

    ret, err = shell.shell_cmd(command=('unset BBPATH; bash -c \"source %s %s;\"' 
                                % (os.path.join(target_path, 'oe-init-build-env'), os.path.join(target_path, 'build'))), 
                                    cwd=target_path)
    if err == True:
        server.close()
        raise Exception("auto create configure file error: %s" % (ret))
        
    server.close()
    
    bb_path = os.path.join(project_path, project_name, 'bitbake')
    oe_path = os.path.join(project_path, project_name, 'openembedded-core')
    yocto_path = os.path.join(project_path, project_name, 'meta-yocto')

    if os.path.exists(bb_path) == False or os.path.exists(oe_path) == False or os.path.exists(yocto_path) == False:
        raise Exception('Project is not complete')

    return "Project Create Success"

@shared_task(bind=True)
def project_import_task(self, project_path, project_name, url):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', 8866))
    progress_send = ProgressSend(self)
    progress_send.send_progress(percentage=50, description='Clone Project')

    project_repo = git.git_clone(url, project_path, project_name)
    project_repo.start()

    path = os.path.join(project_path, project_name)

    i = 0
    while(os.path.exists(path) == False and i < 3):    

        while project_repo.is_alive():
            try:
                server.settimeout(5)
                byte, addr = server.recvfrom(1024)
            except:
                continue
            gitMessage = json.loads(byte.decode('ascii'))
            sub = [{'percentage': int(gitMessage['cur_count']*100/gitMessage['max_count']), 'description': gitMessage['message']}]
            progress_send.send_progress(percentage=50, subProgress=sub, description='Start Clone Project')               

        if os.path.exists(path):
            break
        else:
            i += 1

    if i == 3:
        raise Exception('git clone error')

    target_path = os.path.join(project_path, project_name)
    bitbake_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bitbake')
    r, err = shell.shell_cmd(command=('cp -r %s %s' % (bitbake_path, target_path)), cwd = target_path)
    if err == True:
        server.close()
        raise Exception("project template build error: %s" % (r))

    m = Migration()
    m.project_import(project_path, project_name)


@shared_task(bind=True)
def meta_clone_task(self, name, url, remote_or_local, subd, project_id):
    # TODO: meta add sub directory, meta add without donwload
    progress_send = ProgressSend(self)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', 8866))
    progress_send.send_progress(percentage=0, description='Check the Exist Meta')
    metas = MetaLayer.objects.filter(project__id=project_id)
    project = Project.objects.get(id=project_id)

    for m in metas:
        if m.name == name and m.sub == subd:
            server.close()
            raise Exception("meta is already exist")

    progress_send.send_progress(33, description='Meta Adding...')

    if project.project_version == 'HARDKNOTT':
        yocto_version = 'hardknott'
    elif project.project_version == 'GATESGARTH':
        yocto_version = 'gatesgarth'
    elif project.project_version == 'DUNFELL':
        yocto_version = 'dunfell'
    elif project.project_version == 'ZEUS':
        yocto_version = 'zeus'

    if remote_or_local == 'remote':
        path = os.path.join(project.project_path, project.project_name, name)
        i = 0
        while(os.path.exists(path) == False and i < 3):
            submodule = git.git_submodule(os.path.join(project.project_path, project.project_name),
                            name, url, yocto_version)
            submodule.start()

            while submodule.is_alive():
                try:
                    server.settimeout(5)
                    byte, addr = server.recvfrom(1024)
                except:
                    continue
                gitMessage = json.loads(byte.decode('ascii'))
                sub = [{'percentage': int(gitMessage['cur_count']*100/gitMessage['max_count']), 'description': gitMessage['message']}]
                progress_send.send_progress(subProgress=sub)
            
            if os.path.exists(path):
                break
            else:
                i += 1

        if i == 3:
            raise Exception('git clone error')

    progress_send.send_progress(66, description='Save Meta-Layer')
    try:
        MetaLayer.objects.create(project=project, 
                        name=name, url=url, remote_or_local=remote_or_local, sub=subd)    
    except:
        server.close()
        raise Exception("meta model create err")

    if subd != '':
        meta_name = name + '/' + subd
    else:
        meta_name = name

    bbcommand.bitbake_addlayer(os.path.join(project.project_path, project.project_name), 
                        os.path.join(project.project_path, project.project_name, meta_name))

    server.close()
    return 'meta add success'

@shared_task(bind=True)
def bitbake_progress(self, project_path, project_name, target, command):
    # TODO: 增加一个锁，确保同一个时刻只有一个 Bitbake 进程
    # TODO: 任务恢复，每次进入任务查询是否有 Bitbake 任务在进行中， 并默认不显示，点击按钮后显示任务进度
    progress_send = ProgressSend(self)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', 6688))

    bitbake = bbcommand.BitbakeThread(os.path.join(project_path, project_name), target, command)
    bitbake.start()

    progress_send = ProgressSend(self)

    lock_file = os.path.join(project_path, project_path, 'build/bitbake.lock')
    if os.path.exists(lock_file):
        raise Exception('Another Bitbake Process')

    start_time = datetime.now().timestamp()

    while True:
        bbprogress_byte, addr = server.recvfrom(8192)
        bbprogress = json.loads(bbprogress_byte.decode('ascii'))
        if bbprogress['event_type'] == 'dianshao_ui_start':
            print('dianshao ui has already started')

        if bbprogress['event_type'] == 'TaskList':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            sub = []
            # TODO: 处理 progress < 0
            for task in bbprogress['tasks']:
                if task['progress'] < 0:
                    sub.append({'percentage': 0, 'description': ('%s pending' % task['title'])})
                else:
                    sub.append({'percentage': task['progress'], 'description': (('%s:%s') %(task['title'], task['rate']))})
            
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s), subProgress=sub)
            continue

        if bbprogress['event_type'] == 'Ping':
            # TODO: Server Command
            # TODO: ping interval
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s))

        if bbprogress['event_type'] == 'End':
            if bbprogress['total_error'] > 0:
                progress_send.send_progress(header='Bitbake Failed', description=bbprogress['summary'])
                raise Exception('Bitbake Failed, With %s errors' % bbprogress['total_error'])
            elif bbprogress['total_task_failures'] > 0:
                progress_send.send_progress(header='Bitbake Failed', description=bbprogress['summary'])
                raise Exception('Bitbake Failed, With %s errors' % bbprogress['total_task_failures'])
            else:
                progress_send.send_progress(header='Bitbake Success', description=bbprogress['summary'])
                return ('Bitbake Success with %s Warnings' % bbprogress['total_warning'])
        
        if bbprogress['event_type'] == 'CommandFailed':
            raise Exception('Bitbake Failed, Please Find Details in dianshao_bitbake.log')
        
        if bbprogress['event_type'] == 'CommandExit':
            break

        if bbprogress['event_type'] == 'CommandCompleted':
            break

        if bbprogress['event_type'] == 'logging.LogRecord':
            print(bbprogress['msg'])
        
        if bbprogress['event_type'] == 'CacheLoadStarted':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s), 
                            percentage=0, description='cache data load started')

        if bbprogress['event_type'] == 'CacheLoadProgress':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s), 
                            percentage=int(int(bbprogress['current'])*100/int(bbprogress['total'])), description='cache data loading')

        if bbprogress['event_type'] == 'CacheLoadCompleted':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s), 
                            percentage=100, description='cache data load succes with %d retry times' % bbprogress['num_entries'])

        if bbprogress['event_type'] == 'ProcessStarted':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s),
                            percentage=0, description='%s process started' % bbprogress['processname'])

        if bbprogress['event_type'] == 'ProcessProgress':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s),
                            percentage=int(bbprogress['progress']), description='%s process excuting' % bbprogress['processname'])
            # TODO: Add Parse Progress
        if bbprogress['event_type'] == 'ProcessFinished':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s),
                            percentage=100, description='%s process finished' % bbprogress['processname'])

        if bbprogress['event_type'] == 'runQueueTaskStarted':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s),
                            percentage=int(int(bbprogress['current'])*100/int(bbprogress['total'])), description='%s scene queue task started' % bbprogress['taskstring'])

        if bbprogress['event_type'] == 'ParseStarted':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s),
                            percentage=0, description='Parse started')

        if bbprogress['event_type'] == 'ParseProgress':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s),
                            percentage=int(int(bbprogress['current'])*100/int(bbprogress['total'])), description='Parsing')
        
        if bbprogress['event_type'] == 'ParseCompleted':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s),
                            percentage=100, description='Parse Completed')

        # TODO: ParseFailed 处理
        # TODO: TaskBase 消息显示
        if bbprogress['event_type'] == 'TaskBase':
            period = datetime.utcnow().timestamp() - start_time
            period_s = "{:.1f}".format(period)
            progress_send.send_progress(header=('Bitbaking... %s seconds' % period_s),
                            description=bbprogress['message'])

        # TODO: bitbake 错误处理
        if bbprogress['event_type'] == 'CommandFailed':
            server.close()
            raise Exception('bitbake target failed with err CommandFailed')

    server.close()
    
    return 'bitbake target success'

@shared_task(bind=True)
def bbfile_task_create(self, name, version, type, project_path, mypackage_id):
    package = MyPackages.objects.get(id=mypackage_id)
    bb = bbfile.DianshaoBBFile(name, version, type)
    bb.create_folder(project_path, package.catagory)
    bb.create_bbfile(mypackage_id)


@shared_task(bind=True)
def bbfile_localfile_import_task(self, name, version, type, project_path, file_name, file_path, mypackage_id):
    package = MyPackages.objects.get(id=mypackage_id)
    bb = bbfile.DianshaoBBFile(name, version, type)
    bb.create_folder(project_path, package.catagory)
    bb.create_local_file(file_path, file_name)


@shared_task(bind=True)
def bbfile_localfile_create_task(self, name, version, type, project_path, file_name, content, mypackage_id):
    package = MyPackages.objects.get(id=mypackage_id)
    bb = bbfile.DianshaoBBFile(name, version, type)
    bb.create_folder(project_path, package.catagory)
    bb.create_local_file(file_name, content)

@shared_task(bind=True)
def machinefile_create_task(self, mymachine_id):
    machine_file = bbfile.DianshaoMachineFile(mymachine_id)
    machine_file.create_machine_file()
    machine_file.create_distro_file()

@shared_task(bind=True)
def imagefile_create_task(self, myimage_id):
    imagefile = bbfile.DianshaoImageFile(myimage_id)
    imagefile.create_image_file()

@shared_task(bind=True)
def config_set_task(self, project_id, machine, distro, pm, pt):
    conf = bbfile.DianshaoConfFile(project_id)
    conf.set_config_file(machine, distro, pm, pt)

@shared_task(bind=True)
def patch_generator_task(self, name, file_path, project_path, package_name, 
        package_version, package_type, catagory, text1, text2):
    patch.patch_generator(name, file_path, project_path, package_name, 
        package_version, package_type, catagory, text1, text2)

@shared_task(bind=True)
def shell_cmd_task(self, cmd, cwd):
    ret, error = shell.shell_cmd(command=cmd, cwd=cwd)
    if error:
        raise Exception(ret)

@shared_task(bind=True)
def project_export_task(self, project_id):
    progress_send = ProgressSend(self)
    progress_send.send_progress(percentage=0, description='project exporting')
    m = Migration()
    m.project_export(project_id)
