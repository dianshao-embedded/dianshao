import time
from tools import shell
import os
from threading import Thread

class BitbakeThread(Thread):
    def __init__(self, path, target, command):
        super().__init__()
        self.path = path
        self.target = target
        self.command = command
        pass

    def run(self):
        self.bitbake = os.path.join(self.path, 'bitbake/bin/bitbake')
        self.env = os.path.join(self.path, 'oe-init-build-env')
        self.builddir = os.path.join(self.path, 'build')
        time.sleep(1)
        ret, err = shell.shell_cmd(command=('unset BBPATH; \
                                            bash -c "source %s %s; \
                                            %s %s -u dianshao -c %s > dianshao_bitbake.log 2>&1"' 
                                            % (self.env, self.builddir, self.bitbake, self.target, self.command)), 
                                    cwd=self.path)
        if err == True:
            raise Exception('bitbake error %s' % ret)
        else:
            return ret

def bitbake_addlayer(project_path, path):
    ret, err = shell.shell_cmd(command=('unset BBPATH; bash -c "source %s %s; %s add-layer %s"' 
                        % (os.path.join(project_path, 'oe-init-build-env'), 
                        os.path.join(project_path, 'build'), 
                        os.path.join(project_path, 'bitbake/bin/bitbake-layers'), path)), cwd=project_path)
    if err == True:
        raise Exception('bitbake error %s' % ret)
    else:
        return ret