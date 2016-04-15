from distutils.core import setup, Extension
from distutils import sysconfig
# SET VS90COMNTOOLS=%VS140COMNTOOLS%

#module1 = Extension('mysum', libraries = ['sum_ext.dll'])

setup (name = 'MySum',
       version = '1.0',
       description = 'This is a sum package',
       py_modules = ['sum'],
       data_files = [(sysconfig.get_python_lib(), ["mymath.dll"])])
