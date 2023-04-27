import socket
import time

s = socket.socket()
host = ''
port = 44444

def setupServer():
    global host, port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("CREATED")

    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)

    print("SOCKET BIND COMPLETE")
    return s

def setupConnection():
    s.listen(1)
    conn, address = s.accept()

    print(f"CONNECTED to {address[0]} : {address[1]}")
    return con

def GET(val):
    return val

def dataTransfer(conn, value):
    conn.sendall(str.encode(value))


def close():
    conn.close()

s = setupServer()

while True:
    global conn
    try:
        conn = setupConnection()
        dataTransfer(conn, "asdf")
    except:
        conn.close()
        break

#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.bind(('', port))
#s.listen(5)
#i=0
#
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
