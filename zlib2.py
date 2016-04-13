from cffi import FFI
import os


bindir = ("C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/"
          "ca0c09cfa678fd91b04c82824988c42e9ac40ddf")

dll = os.path.join(bindir, "bin/zlib.dll")
header = os.path.join(bindir, "include/zlib.h")
dlldir = os.path.join(bindir, "bin")
with open(header, "r") as f:
    header_content = f.read()

include_dirs = [os.path.join(bindir, "include")]

ffi = FFI()
ffi.set_source("_myzlib", header_content, include_dirs=include_dirs,
               library_dirs=[dlldir])


if __name__ == "__main__":
    ffi.compile()