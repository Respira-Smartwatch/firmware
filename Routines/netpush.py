import socket
import time

class NetPusher:
    def __init__(self):
        self.socket = None
        self.conn = None
        self.host = ''
        self.port = 44443
        self.address = None

        self.setupServer()
        self.setupConnection()

    def setupServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("CREATED")

        try:
            self.socket.bind((self.host, self.port))
        except socket.error as msg:
            print(msg)
            return False

        print("SOCKET BIND COMPLETE")
        return self.socket

    def setupConnection(self):
        self.socket.listen(1)
        self.conn, self.address = self.socket.accept()
        print(f"CONNECTED to {self.address[0]} : {self.address[1]}")
        return self.conn


    def data_send(self, value):
        if self.conn:
            self.conn.sendall(str.encode(f"{value}"))
        else:
            return None

    def close(self):
        self.conn.close()
        self.socket.close()

if __name__ == "__main__":
    netPush = NetPusher()
    i = 0
    while True:
        try:
            print(f"sending: {i}")
            netPush.data_send(i)
            i += 1
        except KeyboardInterrupt:
            pass
            #netPush.close()
            #break

#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.bind(('', port))
#s.listen(5)
#i=0
#
#s.close()
#while True:
#    try:
#        c,addr = s.accept()
#        print("CLIENT CONNECTED")
#        while True:
#            if i==1:
#                i=0
#            else:
#                i=1
#            c.send(str(i))
#            time.sleep(1)
#        c.close()
#    except:
#        print("CLIENT DISCCONECT")
