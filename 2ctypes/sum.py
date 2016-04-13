import ctypes, os

sum_ext = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "sum_ext.dll"))
sum_ext.sum.restype = ctypes.c_double  # interpret result as double

def sum(a, b):
  return sum_ext.sum(ctypes.c_float(a), ctypes.c_float(b))
