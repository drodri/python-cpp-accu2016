import mymath

if __name__ == '__main__':
    input = "Hello world, hello world" * 100000
    ct_archive = mymath.deflate(input)
    print "Compression ", len(input), "=>", len(ct_archive)
    ct_orig = mymath.inflate(ct_archive)
    assert ct_orig == input
    print "OK "