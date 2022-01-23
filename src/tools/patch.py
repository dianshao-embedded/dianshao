from .shell import shell_cmd
from .bbfile import DianshaoBBFile
import os

def patch_generator(name, file_path, project_path, package_name, package_version, package_type, catagory, text1, text2):
    fd = DianshaoBBFile(package_name, package_version, package_type)
    fd.create_folder(project_path, catagory)
    fd.create_local_file(name+'-old', text1)
    fd.create_local_file(name+'-new', text2)

    old_path = os.path.join(fd.files_path, name+'-old')
    new_path = os.path.join(fd.files_path, name+'-new')
    patch_path = os.path.join(fd.files_path, name+'.patch')

    shell_cmd(('bash -c "diff -Naur %s %s > %s"'
                    % ( old_path, new_path, patch_path)), project_path)

    os.remove(old_path)
    os.remove(new_path)

    content = open(patch_path, 'r')
    lines = content.readlines()
    lines[0] = '--- .' + file_path + '\n'
    lines[1] = '+++ .' + file_path + '\n'

    content = open(patch_path, 'w')
    content.writelines(lines)
    content.close()
    