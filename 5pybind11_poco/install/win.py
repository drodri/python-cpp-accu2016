import os
import shutil
import tempfile


def main(compiled_path):
    folder_tmp = tempfile.mkdtemp(suffix='pypoco')
    resources = os.path.join(os.path.dirname(__file__), 'resources/windows/')
    print 'Copying %s to %s' % (resources, os.path.join(folder_tmp, 'installdata'))
    shutil.copytree(resources,  os.path.join(folder_tmp, 'installdata'))

    print 'Copying %s to %s' % (compiled_path,
                                os.path.join(folder_tmp, 'installdata', 'pypoco'))
    shutil.copytree(compiled_path, os.path.join(folder_tmp, 'installdata', 'pypoco'))

    iss_path = os.path.join(folder_tmp, 'installdata', 'installer.iss')

    command = []
    command.append('"ISCC.exe"')
    command.append(os.path.join(folder_tmp, 'installdata', 'installer.iss'))
    command = " ".join(command)
    print command
    os.system(command)

    print(str(folder_tmp))
