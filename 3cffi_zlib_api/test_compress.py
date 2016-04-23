import os
import ctypes
from ctypes import create_string_buffer
from _myzlib import ffi

_zlib = ffi.dlopen( "zlib.dll")

ZLIB_VERSION = "1.2.8"
Z_NULL = 0
Z_OK = 0
Z_STREAM_END = 1
Z_NO_FLUSH = 0
Z_FINISH = 4
CHUNK = 1024 * 32

def compress(input, level=6):
    out = []
    st = ffi.new("z_stream*")
    st.avail_in  = len(input)
    st.next_in   = ffi.new("char[]", input)
    st.avail_out = 0
    st.next_out = ffi.NULL
    err = _zlib.deflateInit_(st, level, ffi.new("char[]", 
                ZLIB_VERSION), ffi.sizeof("z_stream"))
    st.data_type = 1
    assert err == Z_OK, err
    while True:
        st.avail_out = CHUNK
        outbuf = ffi.new("char[]", CHUNK)
        st.next_out = outbuf
        err = _zlib.deflate(st, Z_FINISH)
        buf = ffi.buffer(outbuf[0:CHUNK-st.avail_out], CHUNK-st.avail_out)
        out.append(buf[:])
        if err == Z_STREAM_END: break
        elif err == Z_OK: pass
        else:
            raise AssertionError, err 
    err = _zlib.deflateEnd(st)
    assert err == Z_OK, err
    return "".join(out)
    
        
def decompress(input):
    out = []
    st = ffi.new("z_stream*")
    st.avail_in  = len(input)
    st.next_in   = ffi.from_buffer(create_string_buffer(input))
    st.avail_out = 0
    st.next_out = ffi.NULL
    err = _zlib.inflateInit2_(st, 15, ffi.new("char[]", ZLIB_VERSION), ffi.sizeof("z_stream"))
    assert err == Z_OK, err
    while True:
        st.avail_out = CHUNK
        outbuf = ffi.from_buffer(create_string_buffer(32768))
        st.next_out = outbuf
        err = _zlib.inflate(st, Z_NO_FLUSH)
        if err in [Z_OK, Z_STREAM_END]: 
            out.append(outbuf[:CHUNK-st.avail_out])
        else:
            raise AssertionError, err 
        if err == Z_STREAM_END: 
            break
    err = _zlib.inflateEnd(st)
    assert err == Z_OK, err
    return "".join(out)

def _test(): 
    input = "Hello world, hello world" * 100000
    ct_archive = compress(input, 6)
    print "Compression ", len(input), "=>", len(ct_archive)
    ct_orig = decompress(ct_archive)
    assert ct_orig == input
    print "OK ", 

if __name__ == '__main__':
    _test()


