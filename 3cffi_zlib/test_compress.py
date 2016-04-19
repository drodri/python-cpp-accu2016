import os
import ctypes
from ctypes import create_string_buffer
from cffi import FFI
ffi = FFI()

bindir = "C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/ca0c09cfa678fd91b04c82824988c42e9ac40ddf/bin" 

ffi.cdef("""typedef void const *voidpc;
typedef void  *voidpf;
typedef void  *voidp;
typedef unsigned int uInt;
   
typedef voidpf (*alloc_func)(voidpf opaque, uInt items, uInt size);
typedef void   (*free_func) (voidpf opaque, voidpf address);
struct internal_state;

typedef struct z_stream_s {
    const unsigned char *next_in;     /* next input byte */
    unsigned int     avail_in;  /* number of bytes available at next_in */
    unsigned long    total_in;  /* total number of input bytes read so far */

    unsigned char    *next_out; /* next output byte should be put there */
    unsigned int   avail_out; /* remaining free space at next_out */
    unsigned long     total_out; /* total number of bytes output so far */

    const unsigned char *msg;  /* last error message, NULL if no error */
    struct internal_state *state; /* not visible by applications */

    alloc_func zalloc;  /* used to allocate the internal state */
    free_func  zfree;   /* used to free the internal state */
    voidpf     opaque;  /* private data object passed to zalloc and zfree */

    int     data_type;  /* best guess about the data type: binary or text */
    unsigned long    adler;      /* adler32 value of the uncompressed data */
    unsigned long    reserved;   /* reserved for future use */
} z_stream;

int deflateInit_(z_stream* strm, int level,
                 const char *version, int stream_size);
int inflateInit2_(z_stream* strm, int  windowBits,
                 const char *version, int stream_size);
int deflate (z_stream* strm, int flush);
int inflate (z_stream* strm, int flush);
int deflateEnd (z_stream* strm);
""")
_zlib = ffi.dlopen(os.path.join(bindir, "zlib.dll"))


ZLIB_VERSION = "1.2.8"
Z_NULL = 0
Z_OK = 0
Z_STREAM_END = 1
Z_NEED_DICT = 2
Z_NO_FLUSH = 0
Z_FINISH = 4
CHUNK = 1024 * 32

def compress(input, level=6):
    out = []
    st = ffi.new("z_stream*")
    st.avail_in  = len(input)
    st.next_in   = ffi.from_buffer(create_string_buffer(input))
    st.avail_out = 0
    st.next_out = ffi.NULL
    err = _zlib.deflateInit_(st, level, ffi.new("char[]", ZLIB_VERSION), ffi.sizeof("z_stream"))
    assert err == Z_OK, err
    while True:
        st.avail_out = CHUNK
        outbuf = ffi.from_buffer(create_string_buffer(CHUNK))
        st.next_out = outbuf
        print "Lets deflate"
        err = _zlib.deflate(st, Z_FINISH)
        print "deflated ", err, st.avail_out, st.avail_in
        print len(outbuf[0:CHUNK-st.avail_out])
        buf = ffi.buffer(outbuf[0:CHUNK-st.avail_out], CHUNK-st.avail_out)
        print "Len ", len(buf)
        out.append(buf[:])
        print "Appended to out"
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


