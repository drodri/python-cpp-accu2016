import ctypes, os

bindir = "C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/ca0c09cfa678fd91b04c82824988c42e9ac40ddf/bin" 
_zlib = ctypes.CDLL(os.path.join(bindir, "zlib.dll"))
_zlib.zlibVersion.restype = ctypes.c_char_p

print "Version ", _zlib.zlibVersion()
