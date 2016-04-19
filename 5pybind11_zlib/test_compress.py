import myzlib

st=z_stream()

ZLIB_VERSION = "1.2.8"
Z_NULL = 0x00
Z_OK = 0x00
Z_STREAM_END = 0x01
Z_NEED_DICT = 0x02
Z_NO_FLUSH = 0x00
Z_FINISH = 0x04
CHUNK = 1024 * 32

def compress(input, level=6):
    out = []
    st = z_stream()
    st.avail_in  = len(input)
    st.next_in   = input
    st.avail_out = Z_NULL
    st.next_out = Z_NULL
    err = myzlib.deflateInit_(st, level, ZLIB_VERSION, len(st))
    assert err == Z_OK, err
    while True:
        st.avail_out = CHUNK
        outbuf = ctypes.create_string_buffer(CHUNK)
        st.next_out = outbuf
        err = myzlib.deflate(st, Z_FINISH)
        out.append(outbuf[:CHUNK-st.avail_out])
        if err == Z_STREAM_END: break
        elif err == Z_OK: pass
        else:
            raise AssertionError, err 
    err = myzlib.deflateEnd(st)
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


