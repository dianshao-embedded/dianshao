from logging import exception
import os
import socket
import json
from celery import shared_task
from progressui.backend import ProgressSend
from git.repo.base import Repo
from tools import shell, git, bbcommand
from .models import MetaLayer, Project

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

    while submodule.is_alive():
        try:
            server.settimeout(5)
            byte, addr = server.recvfrom(1024)
        except:
            continue
        gitMessage = json.loads(byte.decode('ascii'))
        sub = [{'percentage': int(gitMessage['cur_count']*100/gitMessage['max_count']), 'description': gitMessage['message']}]
        progress_send.send_progress(percentage='25',subProgress=sub, description='Add Bitbake Submodule')

    bitbake_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bitbake')
    r, err = shell.shell_cmd(command=('cp -r %s %s' % (bitbake_path, target_path)), cwd = target_path)
    if err == True:
        raise Exception("project template build error: %s" % (r))

    progress_send.send_progress(percentage='50', description='Add Openembedded-Core Submodule')

    submodule = git.git_submodule(target_path, 'openembedded-core',
                    'https://github.com/openembedded/openembedded-core.git',
                    yocto_version)
    submodule.start()
    
    while submodule.is_alive():
        try:
            server.settimeout(5)
            byte, addr = server.recvfrom(1024)
        except:
            continue
        gitMessage = json.loads(byte.decode('ascii'))
        sub = [{'percentage': int(gitMessage['cur_count']*100/gitMessage['max_count']), 'description': gitMessage['message']}]
        progress_send.send_progress(percentage='50', subProgress=sub, description='Add Openembedded-Core Submodule')
    
    project = Project.objects.get(id=project_id)
    MetaLayer.objects.create(project=project, 
                            name='openembedded-core', 
                            url='https://github.com/openembedded/openembedded-core.git')
    
    progress_send.send_progress(percentage='75', description='Add Meta-Yocto Submodule')

    submodule = git.git_submodule(target_path, 'meta-yocto',
                    'https://git.yoctoproject.org/meta-yocto.git',
                    yocto_version)
    submodule.start()

    while submodule.is_alive():
        try:
            server.settimeout(5)
            byte, addr = server.recvfrom(1024)
        except:
            continue
        gitMessage = json.loads(byte.decode('ascii'))
        sub = [{'percentage': int(gitMessage['cur_count']*100/gitMessage['max_count']), 'description': gitMessage['message']}]
        progress_send.send_progress(percentage='75', subProgress=sub, description='Add Meta-Yocto Submodule')               

    MetaLayer.objects.create(project=project,
                            name='meta-yocto', 
                            url='https://git.yoctoproject.org/meta-yocto.git')

    ret, err = shell.shell_cmd(command=('unset BBPATH; bash -c \"source %s %s;\"' 
                                % (os.path.join(target_path, 'oe-init-build-env'), os.path.join(target_path, 'build'))), 
                                    cwd=target_path)
    if err == True:
        raise Exception("auto create configure file error: %s" % (ret))
        
    server.close()
    # TODO: 项目完整性检查
    return "Project Create Success"


@shared_task(bind=True)
def meta_clone_task(self, name, url, project_id):
    # TODO: meta add sub directory, meta add without donwload
    progress_send = ProgressSend(self)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', 8866))
    progress_send.send_progress(percentage=0, description='Check the Exist Meta')
    metas = MetaLayer.objects.filter(project__id=project_id)
    project = Project.objects.get(id=project_id)

    for m in metas:
        if m.name == name:
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

    progress_send.send_progress(66, description='Save Meta-Layer')
    try:
        MetaLayer.objects.create(project=project, name=name, url=url)    
    except:
        raise Exception("meta model create err")

    bbcommand.bitbake_addlayer(os.path.join(project.project_path, project.project_name), 
                        os.path.join(project.project_path, project.project_name, name))

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

    while True:
        bbprogress_byte, addr = server.recvfrom(8192)
        print(bbprogress_byte)
        bbprogress = json.loads(bbprogress_byte.decode('ascii'))
        if bbprogress['event_type'] == 'dianshao_ui_start':
            print('dianshao ui has already started')

        if bbprogress['event_type'] == 'TaskList':
            sub = []
            # TODO: 处理 progress < 0
            for task in bbprogress['tasks']:
                sub.append({'percentage': task['progress'], 'description': (('%s:%s') %(task['title'], task['rate']))})
            
            progress_send.send_progress(subProgress=sub)
            continue

        if bbprogress['event_type'] == 'CommandCompleted':
            break

        if bbprogress['event_type'] == 'CacheLoadStarted':
            progress_send.send_progress(percentage=0, description='cache data load started')

        if bbprogress['event_type'] == 'CacheLoadProgress':
            progress_send.send_progress(percentage=int(int(bbprogress['current'])*100/int(bbprogress['total'])), description='cache data loading')

        if bbprogress['event_type'] == 'CacheLoadCompleted':
            progress_send.send_progress(percentage=100, description='cache data load succes with %d retry times' % bbprogress['num_entries'])

        if bbprogress['event_type'] == 'ProcessStarted':
            progress_send.send_progress(percentage=0, description='%s process started' % bbprogress['processname'])

        if bbprogress['event_type'] == 'ProcessProgress':
            progress_send.send_progress(percentage=int(bbprogress['progress']), description='%s process excuting' % bbprogress['processname'])

        if bbprogress['event_type'] == 'ProcessFinished':
            progress_send.send_progress(percentage=100, description='%s process finished' % bbprogress['processname'])

        if bbprogress['event_type'] == 'runQueueTaskStarted':
            progress_send.send_progress(percentage=int(int(bbprogress['current'])*100/int(bbprogress['total'])), description='%s scene queue task started' % bbprogress['taskstring'])

        # TODO: ParseFailed 处理
        # TODO: TaskBase 消息显示
        if bbprogress['event_type'] == 'event_type':
            progress_send.send_progress(description=bbprogress['message'])

        # TODO: bitbake 错误处理
        if bbprogress['event_type'] == 'CommandFailed':
            raise exception('bitbake target failed with err CommandFailed')

    server.close()

    return 'bitbake target success'

    