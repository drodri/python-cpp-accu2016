from _mymath import ffi
lib = ffi.dlopen("mymath.dll") 

def sum(a, b):
  return lib.sum(a, b)

if __name__ == "__main__":
  print sum(2.1, 3.2)