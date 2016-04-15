import ctypes, os

mymath = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "mymath.dll"))
mymath.sum.restype = ctypes.c_double  # interpret result as double

def sum(a, b):
  return mymath.sum(ctypes.c_float(a), ctypes.c_float(b))
