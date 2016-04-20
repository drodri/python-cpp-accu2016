from cffi import FFI
ffi = FFI()
ffi.set_source("_myzlib", """ // passed to the real C compiler
        #include "zlib.h"
    """,
    include_dirs = ['C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/ca0c09cfa678fd91b04c82824988c42e9ac40ddf/include'],
        libraries = ["zlib"],
        library_dirs  = ['C:/Users/drodri/.conan/data/zlib/1.2.8/lasote/stable/package/ca0c09cfa678fd91b04c82824988c42e9ac40ddf/lib'],
       )

ffi.cdef("""

typedef struct z_stream_s {
    const unsigned char *next_in;     /* next input byte */
    unsigned int     avail_in;  /* number of bytes available at next_in */
    unsigned char    *next_out; /* next output byte should be put there */
    unsigned int   avail_out; /* remaining free space at next_out */
    unsigned long total_in;
    unsigned long total_out;
    int data_type;
    ...;     // literally dot-dot-dot
} z_stream;

int deflateInit_(z_stream* strm, int level,
                 const char *version, int stream_size);
int deflate (z_stream* strm, int flush);
int deflateEnd (z_stream* strm);

int inflateInit2_(z_stream* strm, int  windowBits,
                 const char *version, int stream_size);
                 int inflate (z_stream* strm, int flush);
""")

if __name__ == "__main__":
    ffi.compile()
