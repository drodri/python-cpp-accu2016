import mymath

print mymath.add(2.1, 3.2)
for i in range(10):
    print mymath.random()


import ctypes
csuma = ctypes.CDLL("sumadl.dll")
csuma.suma.restype = ctypes.c_double  # Very important, interpret result as float
print csuma.suma(ctypes.c_float(2.1), ctypes.c_float(3.2))


from cffi import FFI
ffi = FFI()
ffi.cdef("float suma(float a, float b);")
ffi_suma = ffi.dlopen("sumadl.dll")
print ffi_suma.suma(3.4, 5.7)
