#create an INET, STREAMing socket
import socket
import time
s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
s.connect(("rt.joinuptaxi.com", 55555))
print "Connected"
s.settimeout(2)

s.send("{type: KeepAlive}")

while True:
    print "Lets receive"
    chunk = s.recv(1)
    print "REceived chunk ", chunk
    if chunk == '':
        raise RuntimeError("socket connection broken")
    print chunk
