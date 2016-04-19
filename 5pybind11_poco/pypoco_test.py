import sys
import pypoco

if __name__ == '__main__':
    r = pypoco.Random()
    for i in range(10):
        print r.nextFloat()
    sys.exit(0)


