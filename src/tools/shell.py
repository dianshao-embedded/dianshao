# Shell 调用函数

import os
import subprocess

def shell_cmd(command, cwd, nowait=False):

    env=os.environ.copy()
    
    p = subprocess.Popen(command, cwd = cwd, shell=True, stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, env=env)

    if nowait:
        return
    (out,err) = p.communicate()
    p.wait()
    # TODO: shell 返回功能还需要考虑下
    if p.returncode:
        if len(err) == 0:
            ret = "command: %s \n%s" % (command, out)
        else:
            ret = "command: %s \n%s" % (command, err)
        return ret, True
    else:
        ret = "command: %s \n%s" % (command, out)
        return ret, False
