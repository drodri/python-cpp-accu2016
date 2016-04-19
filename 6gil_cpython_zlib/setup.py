from distutils.core import setup, Extension

# SET VS90COMNTOOLS=%VS140COMNTOOLS%

module1 = Extension('mymath', sources = ['mymath.cpp'],
        include_dirs = ['C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/ca0c09cfa678fd91b04c82824988c42e9ac40ddf/include'],
        libraries = ["zlib"],
        library_dirs  = ['C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/ca0c09cfa678fd91b04c82824988c42e9ac40ddf/lib'],
       )

setup (name = 'MyMaths',
       version = '1.0',
       description = 'This is a math package',
       ext_modules = [module1])
