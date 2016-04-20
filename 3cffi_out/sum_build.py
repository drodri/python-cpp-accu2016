from cffi import FFI
ffi = FFI()
ffi.set_source("_mymath", None)
ffi.cdef("float sum(float a, float b);")

if __name__ == "__main__":
    ffi.compile()
