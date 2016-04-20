import ctypes, os

_zlib = ctypes.CDLL("zlib.dll")
_zlib.zlibVersion.restype = ctypes.c_char_p

print "Version ", _zlib.zlibVersion()
