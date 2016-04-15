import ctypes, os

bindir = "C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/ca0c09cfa678fd91b04c82824988c42e9ac40ddf/bin" 
_zlib = ctypes.CDLL(os.path.join(bindir, "zlib.dll"))

# Work by https://gist.github.com/colinmarc/2152055
__license__ = """
Copyright (c) 2009-2012 Mark Nottingham <mnot@pobox.com>
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class _z_stream(ctypes.Structure):
    _fields_ = [
        ("next_in", ctypes.POINTER(ctypes.c_ubyte)),
        ("avail_in", ctypes.c_uint),
        ("total_in", ctypes.c_ulong),
        ("next_out", ctypes.POINTER(ctypes.c_ubyte)),
        ("avail_out", ctypes.c_uint),
        ("total_out", ctypes.c_ulong),
        ("msg", ctypes.c_char_p),
        ("state", ctypes.c_void_p),
        ("zalloc", ctypes.c_void_p),
        ("zfree", ctypes.c_void_p),
        ("opaque", ctypes.c_void_p),
        ("data_type", ctypes.c_int),
        ("adler", ctypes.c_ulong),
        ("reserved", ctypes.c_ulong),     
    ]

# TODO: get zlib version with ctypes
ZLIB_VERSION = ctypes.c_char_p("1.2.8")
Z_NULL = 0x00
Z_OK = 0x00
Z_STREAM_END = 0x01
Z_NEED_DICT = 0x02
Z_NO_FLUSH = 0x00
Z_FINISH = 0x04
CHUNK = 1024 * 32

def compress(input, level=6):
    out = []
    st = _z_stream()
    st.avail_in  = len(input)
    st.next_in   = ctypes.cast(ctypes.c_char_p(input), ctypes.POINTER(ctypes.c_ubyte))
    st.avail_out = Z_NULL
    st.next_out = ctypes.cast(Z_NULL, ctypes.POINTER(ctypes.c_ubyte))
    err = _zlib.deflateInit_(ctypes.byref(st), level, ZLIB_VERSION, ctypes.sizeof(st))
    assert err == Z_OK, err
    while True:
        st.avail_out = CHUNK
        outbuf = ctypes.create_string_buffer(CHUNK)
        st.next_out = ctypes.cast(outbuf, ctypes.POINTER(ctypes.c_ubyte))
        err = _zlib.deflate(ctypes.byref(st), Z_FINISH)
        out.append(outbuf[:CHUNK-st.avail_out])
        if err == Z_STREAM_END: break
        elif err == Z_OK: pass
        else:
            raise AssertionError, err 
    err = _zlib.deflateEnd(ctypes.byref(st))
    assert err == Z_OK, err
    return "".join(out)
    
        
def decompress(input):
    out = []
    st = _z_stream()
    st.avail_in  = len(input)
    st.next_in   = ctypes.cast(ctypes.c_char_p(input), ctypes.POINTER(ctypes.c_ubyte))
    st.avail_out = Z_NULL
    st.next_out = ctypes.cast(Z_NULL, ctypes.POINTER(ctypes.c_ubyte))
    err = _zlib.inflateInit2_(ctypes.byref(st), 15, ZLIB_VERSION, ctypes.sizeof(st))
    assert err == Z_OK, err
    while True:
        st.avail_out = CHUNK
        outbuf = ctypes.create_string_buffer(CHUNK)
        st.next_out = ctypes.cast(outbuf, ctypes.POINTER(ctypes.c_ubyte))
        err = _zlib.inflate(ctypes.byref(st), Z_NO_FLUSH)
        if err in [Z_OK, Z_STREAM_END]: 
            out.append(outbuf[:CHUNK-st.avail_out])
        else:
            raise AssertionError, err 
        if err == Z_STREAM_END: 
            break
    err = _zlib.inflateEnd(ctypes.byref(st))
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


