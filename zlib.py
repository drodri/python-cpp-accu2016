from cffi import FFI
import os


bindir = ("C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/"
          "ca0c09cfa678fd91b04c82824988c42e9ac40ddf")

dll = os.path.join(bindir, "bin/zlib.dll")

ffi = FFI()
ffi_zlib = ffi.dlopen(dll)
ffi.cdef("const char * zlibVersion(void);")
version = ffi_zlib.zlibVersion()
print ffi.string(version)
