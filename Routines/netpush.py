import socket
import time

s = socket.socket()
port = 44444
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
s.listen(5)
i=0
while True:
    try:
        c,addr = s.accept()
        print("CLIENT CONNECTED")
        while True:
            if i==1:
                i=0
            else:
                i=1
            c.send(str(i))
            time.sleep(1)
        c.close()
    except:
        print("CLIENT DISCCONECT")
