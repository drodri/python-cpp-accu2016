import os, sys, platform, subprocess, shutil


def _install_pyinstaller(pyinstaller_path):
    # try to install pyinstaller if not installed
    if not os.path.exists(pyinstaller_path):
        subprocess.call('git clone https://github.com/pyinstaller/pyinstaller.git',
                        cwd=os.path.curdir, shell=True)
        subprocess.call('git checkout v2.1', cwd=pyinstaller_path, shell=True)


def _run_bin(bin_path):
    # run the binary to test if working
    pypoco_bin = os.path.join(bin_path, 'pypoco_test')
    retcode = os.system(pypoco_bin)
    if retcode != 0:
        raise Exception("Binary not working")


def pyinstall():
    # Make sure to have the version of PyInstaller
    pyinstaller_path = os.path.join(os.path.curdir, 'pyinstaller')
    _install_pyinstaller(pyinstaller_path)
    
    source_folder = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
    sys.path.append(source_folder)
    
    # Remove old folder, ensure clean build
    try:
        shutil.rmtree(os.path.join(pyinstaller_path, 'pypoco_test'))
    except Exception as e:
        print "Unable to remove old folder", e

    # Invoke pyinstaller
    pypoco_path = os.path.join(source_folder, 'pypoco_test.py')
    subprocess.call('python pyinstaller.py -y -p %s --console %s' % (source_folder, pypoco_path),
                    cwd=pyinstaller_path, shell=True)
                    
    # Execute the binary, to make sure it is OK
    bin_path = os.path.join(pyinstaller_path, 'pypoco_test', 'dist', 'pypoco_test')
    bin_path = os.path.abspath(bin_path)          
    _run_bin(bin_path)

    return bin_path
