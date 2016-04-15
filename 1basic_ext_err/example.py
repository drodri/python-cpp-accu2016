import mymath

print mymath.divide(10, 5)

try:
    print mymath.divide(3, 0)
except Exception as e:
    print type(e), e

try:
    print mymath.divide(3.2, 2)
except Exception as e:
    print type(e), e

try:
    print mymath.divide(0, 0)
except Exception as e:
    print type(e), e