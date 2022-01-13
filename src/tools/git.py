import os
from pathlib import Path
from threading import Thread
from git import Repo
from git.remote import RemoteProgress
import json
import socket

class git_submodule(Thread):
    def __init__(self, father_path, repo_name, repo_url, repo_branch):
        super().__init__()
        self.father_path = father_path
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.repo_branch = repo_branch
    
    def run(self):
        module_file = Path(os.path.join(self.father_path, '.gitmodules'))
        module_file.touch(exist_ok=True)
        fp = open(module_file, 'a', encoding='utf-8')
        fp.write('[submodule "%s"]\n' % self.repo_name)
        fp.write('\tpath = %s\n' % self.repo_name)
        fp.write('\turl = %s\n' % self.repo_url)
        fp.write('\tbranch = %s\n' % self.repo_branch)

        try:
            repo = Repo.clone_from(url=self.repo_url,
                            to_path=os.path.join(self.father_path, self.repo_name),
                            progress=GitProgress())
        except:
            raise Exception("%s clone error" % self.repo_name)

        try:
            repo.git.checkout(self.repo_branch)
        except:
            raise Exception("%s checkout error" % self.repo_name)

        return 'add submodule success'


class git_clone(Thread):
    def __init__(self, repo_url, father_path, repo_name):
        self.father_path = father_path
        self.repo_name = repo_name
        self.repo_url = repo_url
        super().__init__()

    def run(self):
        try:
            repo = Repo.clone_from(url=self.repo_url,
                            to_path=os.path.join(self.father_path, self.repo_name),
                            progress=GitProgress())
            
            repo.submodule_update(progress=GitProgress())

        except:
            raise Exception("%s clone error" % self.repo_name)


class GitProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target = ('127.0.0.1', 8866)

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.client.sendto(json.dumps(
            {'op_code': op_code, 'cur_count': cur_count, 
            'max_count': max_count, 'message': message}).encode('ascii'), 
            self.target)        