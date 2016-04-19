import win
from pyinstaller import pyinstall
import os
import shutil
import sys
import re


def pack():
    # Create exes bundles from python
    compiled_path = pyinstall()

    # Now create specific OS bundl
    retcode = win.main(compiled_path)
    sys.exit(retcode)


if __name__ == '__main__':
    pack()