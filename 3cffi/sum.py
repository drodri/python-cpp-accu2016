from cffi import FFI
ffi = FFI()
ffi.cdef("float sum(float a, float b);")
ffi_suma = ffi.dlopen("sum_ext.dll")

def sum(a, b):
  return ffi_suma.sum(3.4, 5.7)