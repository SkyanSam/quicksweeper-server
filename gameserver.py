import base
import number_guess
import area_attack
import socket
from pathlib import Path
import ssl
import certifi
import os

# Create a context, just like as for the server
server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_context.verify_mode = ssl.CERT_REQUIRED
client_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client_context.verify_mode = ssl.CERT_REQUIRED

#DHE-RSA-AES128-SHA256
print(server_context.get_ciphers())
#server_context.set_ciphers('ECDHE+AESGCM:!ECDSA') not necessary??
#client_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
# Load the server's CA
#context.load_verify_locations(certifi.where())
server_context.load_verify_locations("./certificate.pem")
client_context.load_verify_locations("./certificate.pem")
#context.load_verify_locations(cafile=os.path.relpath(certifi.where()),capath=None,cadata=None)
# Wrap the socket, just as like in the server.
#context.wrap_socket(s, server_hostname='10.0.0.112')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.IPPROTO_TLS)
t = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.IPPROTO_TLS)
s = server_context.wrap_socket(s, server_hostname='10.0.0.112')
t = server_context.wrap_socket(t, server_hostname='10.0.0.112')

#addr='192.168.124.118'
#addr='192.168.162.118'
#s.bind(('10.144.119.197',80))
#s.bind(('192.168.1.240',8000))
#addr='73.133.51.103'
#addr='localhost'
addr='10.0.0.112'
#addr='192.168.0.37'
#addr = '192.168.1.240'
#addr = '192.168.137.1'
s.bind((addr,8000))
t.bind((addr,80))
#s.bind(('172.20.10.2',8000))




s.listen()
s.setblocking(False)
t.listen()
t.setblocking(False)

#s = ssl.wrap_socket (s, certfile='./certificate.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLS)
#t = ssl.wrap_socket (t, certfile='./certificate.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLS)
#s = ssl.wrap_socket(s, certfile='./certificate.pem', keyfile='./key.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLS)
#t = ssl.wrap_socket(t, certfile='./certificate.pem', keyfile='./key.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLS)

#r'test.html
clientCode = ""
with open(str(Path(__file__).parent.absolute())+r'\\test.html') as f:
    clientCode=f.read()
games = {}
cList=[]
waitroom=[]
pList=[]
pDict={}
while True:
    try:
        (connection,address)=t.accept()
        #connection = ssl.wrap_socket(connection, certfile='./certificate.pem', keyfile='./key.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLS)
        #connection = client_context.wrap_socket(connection, server_hostname='10.0.0.112')
        #connection.recv = connection.ssl_read
        #connection.send = connection.ssl_write
        #connection.send(("""HTTP/1.1 200 OK"""+clientCode).encode())
    except BlockingIOError:
        pass
    try:
        (connection,address)=s.accept()
        cList.append(connection)
    except BlockingIOError:
        pass
    for c in cList:
        try:
            #code=c.recv(1)
            code=c.recv(0)
            print(code)
            if code==b'l':
                cList.remove(c)
                c=base.lengthPlayer(c)
                waitroom.append(c)
            if code==b'G':
                #handshake=c.recv(1000)
                handshake=c.recv(1000)
                cList.remove(c)
                c=base.websocketPlayer(c,handshake)
                print('ws')
                waitroom.append(c)
            c.send(b'Send your name.')
        except BlockingIOError:
            pass
    for p in waitroom:
        try:
            name=p.receive()
            if name:
                print(name)
                name=name.decode()
                if '\n' in name:
                    p.send(b'Names cannot contain newlines.')
                elif name in pDict:
                    pDict[name].reconnect(p)
                    waitroom.remove(p)
                else:
                    p.name=name
                    waitroom.remove(p)
                    pList.append(p)
                    pDict[name]=p
        except BlockingIOError:
            pass
        except Exception as e:
            print(e)
            print('Connection closed?')
            waitroom.remove(p)
            pass
    for p in pList:
        try:
            msg=p.receive()
            if msg:
                code=msg[0]
                msg=msg[1:]
                print(code)
                if code==b'n'[0]:
                    l=msg.split(b'\n',2)
                    print(l)
                    name=l[0].decode()
                    typ=l[1].decode()
                    data=l[2]
                    if name in games:
                        p.send(b'This name is already in use.')
                    if typ not in base.gameTypes:
                        p.send(b'This game type is not supported.')
                    else:
                        games[name]=base.gameTypes[typ](data)
                if code==b'j'[0]:
                    name=msg.decode()
                    if games[name].addPlayer(p):
                        pList.remove(p)
                    else:
                        p.send(b'Rejected from game')
                if code==b'g'[0]:
                    bl=b''
                    for name in games:
                        bl+=name.encode()+b'\n'
                    bl=bl[:-1]
                    p.send(bl)
        except BlockingIOError:
            pass
        except Exception as e:
            print(e)
            print('Connection closed?')
            pList.remove(p)
            pass
    deleted=[]
    for g in games:
        for p in games[g].playerList:
            try:
                d=p.receive()
                if d:
                    if d[0]==0:
                        games[g].playerList.remove(p)
                        pList.append(p)
                        if len(games[g].playerList)==0:
                            deleted.append(g)
                    elif d[0]==1:
                        games[g].process(p,d[1:])
                    else:
                        games[g].process(p,d)
            except BlockingIOError:
                pass
            except Exception as e:
                #raise e
                print(e)
                print('Connection closed?')
                p.disconnect()
    for g in deleted:
        del games[g]
