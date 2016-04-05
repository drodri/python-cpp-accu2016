from distutils.core import setup, Extension

module1 = Extension('mymath', sources = ['suma.c'])

setup (name = 'MyMaths',
       version = '1.0',
       description = 'This is a math package',
       ext_modules = [module1])
