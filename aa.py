import random
import base64
import hashlib
import time
class game:
    def __init__(self, addPlayer, process):
        self.process=lambda p,d: process(self,p,d)
        self.addPlayer=lambda p: addPlayer(self, p)
        self.playerList=[]
        self.playersJoined=0
class player:
    def __init__(self, connection, send, receive):
        self.connection=connection
        self.receive=lambda:receive(self)
        self.send=lambda msg:send(self,msg)
def lengthPlayer(connection):
    def send(self, msg):
        l=len(msg)
        ll=[]
        while l>0:
            ll.append(l%255)
            l//=255
        b=bytes(ll[-1-i] for i in range(len(ll)))
        b+=b'\xff'+msg
        self.connection.send(b)
    def receive(self):
        try:
            l=0
            b=self.connection.recv(1)[0]
            while b!=255:
                l=255*l+b
                b=self.connection.recv(1)[0]
            msg=self.connection.recv(l)
            return msg
        except BlockingIOError:
            return False
    return player(connection, send, receive)
'''class taskList:
    def __init__():
        self.front=[]
        self.back=[]
    def enqueue(self,x):
        self.back.append(x)
    def dequeue(self):
        if len(self.front)>0:
            return self.front.pop()
        while len(self.back)>0:
            self.front.append(self.back.pop())
        return self.front.pop()'''
def websocketPlayer(connection, handshake):
    d = [l.split(': ') for l in handshake.decode().split('\r\n')]
    print(d)
    d = {l[0]:l[-1] for l in d}
    response='''HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: '''
    m=hashlib.sha1()
    m.update((d['Sec-Websocket-Key']+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode())
    response+=base64.b64encode(m.digest()).decode()+'\r\n\r\n'
    connection.send(response.encode())
    def send(self, msg):
        self.connection.send(b'\x81'+bytes([len(msg)])+msg)
    def receive(self):
        try:
            code=self.connection.recv(2)
            l=code[1]%128
            if code[0]%16==8:
                print('Connection closed')
                raise Exception
            if l==126:
                l=self.connection.recv(2)
                l=256*el[0]+el[1]
            elif l==127:
                l=self.connection.recv(4)
                l=l[3]+256*l[2]+65536*l[1]+16774656*l[0]
            if code[1]//128:
                mask=self.connection.recv(4)
            else:
                mask=b'\x00\x00\x00\x00'
            data=self.connection.recv(l)
            data=bytes(data[i]^mask[i%4] for i in range(len(data)))
            if code[0]%16==10:
                self.connection.send(b'\x8A'+bytes[l]+data)
                return False
            else:
                return data
        except BlockingIOError:
            return False
    return player(connection,send,receive)
'''def minesweepBot(timeout):
    
    def send(self,message):
        l=message.decode().split('\n',2)
        x=l[0]
        y=l[1]
        code=l[2][0]
        data=l[2][1:]
        if code=='c':
            self.board[x][y]=int(data)
        if code=='o':
            self.board[x][y]=data
        if code=='m':
            if data=='Attack mode has started.':
                self.stage=1
        if code=='s':
            if data=='y' or data=='o':
                self.board[x][y]=False
            if data=='N':
                self.board[x][y]=None
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i>=0 and i<=len(self.board) and j>=0 and j<=self.board and self.board[i][j] not in ['empty', 'mine', 'removed', 'other']
                    self.tasks.push(i,j,time.time()))
    def receive(self):
        if len(tasks)>0:
            for i in range(len(tasks)-1,-1,-1):
                (x,y,t)=self.tasks[i]
            if time.time()-t>=timeout:
                if type(self.board[x][y])==type(0):
                    mineNum'''
                
        
def guessTheNumber(lower, upper):
    def addPlayer(self,p):
        self.playerList.append(p)
        self.playersJoined+=1
        p.send(b'Guess the number!')
        return True
    def process(self,p,d):
        print(process)
        d=int(d)
        if d==self.n:
            p.send(('You win! The number was '+str(self.n)+'. Choosing a new number...').encode())
            self.n=random.randint(lower,upper)
        else:
            p.send(b'Incorrect')
    g=game(addPlayer, process)
    g.n=random.randint(lower,upper)
    return g
def soloMinesweeper(boardsize, pMine):
    def addPlayer(self, p):
        if self.playersJoined>0:
            p.send('This game is full.')
            return False
        
        self.playerList.append(p)
        self.playersJoined+=1
        self.started=False
        self.named=False
        p.send('Send your name.')
        return True
    def process(self,p,d):
        print('processing')
        if not self.named:
            print('starting naming')
            p.name=d.decode()
            p.send('Your name is '+p.name+'.')
            self.named=True
            return
        print('named')
        l=d.split(b'\n')
        x=int(l[0])
        y=int(l[1])
        if not self.started:
            self.numMines=0
            self.squaresFound=0
            self.board=[[0]*boardsize for i in range(boardsize)]
            for i in range(boardsize):
                for j in range(boardsize):
                    if abs(i-x)>1 or abs(j-y)>1:
                        if random.random()<pMine:
                            self.board[i][j]=1
                            self.numMines+=1
            p.send(str(x)+'\n'+str(y)+'\n'+'0')
            self.board[x][y]=p.name
            self.squaresFound=1
            self.started=True
        else:
            if self.board[x][y]==1:
                p.send('You lose.')
            elif self.board[x][y]==0 or self.board[x][y]==p.name:
                if self.board[x][y]==0:
                    self.squaresFound+=1
                self.board[x][y]=p.name
                n=0
                for i in range(x-1,x+2):
                    for j in range(y-1,y+2):
                        if i>=0 and i<boardsize and j>=0 and j<boardsize:
                            if self.board[i][j]==1:
                                n+=1
                p.send(str(x)+'\n'+str(y)+'\n'+str(n))
                if self.squaresFound+self.numMines==boardsize*boardsize:
                    p.send('You win!')
            else:
                p.send(str(x)+'\n'+str(y)+'\n'+self.board[x][y])
    return game(addPlayer, process)
def message(p,m):
    p.send(('0\n0\nm'+m).encode())
def inBoard(self,x,y):
    return 0<=x and x<self.boardsize and 0<=y and y<self.boardsize
def isFrozen(self,p):
    if p.frozen:
        if time.time()-p.frozen>=self.freezeTime:
            p.frozen=False
            return False
        return True
def adjacentClaimed(self,p,x,y):
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if inBoard(self,i,j):
                if self.board[i][j]==p.name:
                    return True
    return False
def freezeLegalMove(self,p,x,y):
    if p.spectating:
        return False
    if not self.started:
        message(p,'Wait for all players to choose a starting square.')
        return False
    if not inBoard(self,x,y):
        return False
    if isFrozen(self,p):
        message(p,'You are frozen.')
        return False
    return True
def freezeMineSelect(self,p,x,y):
    p.frozen=time.time()
    for player in self.playerList:
        player.send((str(x)+'\n'+str(y)+'\nf'+p.name).encode())
def attackLegalMove(self,p,x,y):
    if p.spectating:
        return False
    if not self.started:
        message(p,'Wait for all players to choose a starting square.')
        return False
    if not inBoard(self,x,y):
        return False
    if not adjacentClaimed(self,p,x,y):
        message(p,'You can only claim squares adjacent to your area.')
        return False
    if self.board[x][y]==None:
        return False
    return True
def mineCount(self,x,y):
    c=0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if inBoard(self,i,j):
                if self.board[i][j]==1:
                    c+=1
    return c
def claimSquare(self,n,x,y):
    self.board[x][y]=n
    for player in self.playerList:
        if player.name==n:
            player.send((str(x)+'\n'+str(y)+'\nc'+str(mineCount(self,x,y))).encode())
        else:
            player.send((str(x)+'\n'+str(y)+'\no'+str(n)).encode())
def removeSquare(self,x,y):
    self.numMines-=1
    self.board[x][y]=None
    for p in self.playerList:
        p.send((str(x)+'\n'+str(y)+'\nsN').encode())
    self.squaresRemoved+=1
def resetSquare(self,x,y):
    if self.board[x][y]==1:
        self.numMines-=1
    for p in self.playerList:
        if p.name==self.board[x][y]:
            p.squaresFound-=1
            self.squaresFound-=1
            p.send((str(x)+'\n'+str(y)+'\nsy').encode())
        else:
            p.send((str(x)+'\n'+str(y)+'\nso').encode())
    self.board[x][y]=0
def attackMineSelect(self,p,x,y):
    removeSquare(self,x,y)
    for i in range(x-3,x+4):
        for j in range(y-3,y+4):
            if inBoard(self,i,j) and self.board[i][j]!=None:
                resetSquare(self,i,j)
                if random.random()<self.pMine:
                    self.board[i][j]=1
                    self.numMines+=1
    for i in range(x-4,x+5):
        for j in range(y-4,y+5):
            if inBoard(self,i,j) and self.board[i][j]!=None:
                if abs(x-i)==4 or abs(y-j)==4:
                    for player in self.playerList:
                        if player.name==self.board[i][j]:
                            player.send((str(i)+'\n'+str(j)+'\nc'+str(mineCount(self,i,j))).encode())
def areaAttackLegalMove(self,p,x,y):
    if self.stage==0:
        if self.squaresFound+self.numMines+self.squaresRemoved>=.8*self.boardsize*self.boardsize:
            self.stage=1
            self.attackTime=time.time()
            for player in self.playerList:
                message(player,'Attack mode has started.')
            return areaAttackLegalMove(self,p,x,y)
        else:
            return freezeLegalMove(self,p,x,y)
    else:
        if isFrozen(self,p):
            return False
        if time.time()-self.attackTime>180:
                for player in self.playerList:
                    message(player,'Game over. Your score was '+str(player.squaresFound))
                    return False
        return attackLegalMove(self,p,x,y)
def areaAttackMineSelect(self,p,x,y):
    if self.stage==0:
        return freezeMineSelect(self,p,x,y)
    else:
        return attackMineSelect(self,p,x,y)
        
def Minesweeper(boardsize, pMine, isLegal, mineSelect):
    def addPlayer(self, p):
        p.send(('multiplayer minesweeper\n'+str(boardsize)+'\n'+str(pMine)).encode())
        if self.started:
            message(p,'This game has already started. You are a spectator.')
            p.spectating=True
            p.started=True
        else:
            p.spectating=False
            p.started=False
            for q in self.playerList:
                if q!=p:
                    q.send(('0\n0\nj'+p.name).encode())
        self.playersJoined+=1
        p.frozen=False
        p.squaresFound=0
        self.playerList.append(p)
        for q in self.playerList:
            if q!=p:
                p.send(('0\n0\nj'+q.name).encode())
        for x in range(self.boardsize):
            for y in range(self.boardsize):
                if self.board[x][y]==None:
                    p.send((str(x)+'\n'+str(y)+'\nsN').encode())
                elif self.board[x][y]!=0 and self.board[x][y]!=1:
                    p.send((str(x)+'\n'+str(y)+'\no'+self.board[x][y]).encode())
        return True
    def process(self,p,d):
        l=d.split(b'\n')
        x=int(l[0])
        y=int(l[1])
        if not p.started:
            initSelection(self,p,x,y)
            return
        if not self.isLegal(self,p,x,y):
            return False
        if self.board[x][y]==1:
            self.mineSelect(self,p,x,y)
        elif self.board[x][y]==0 or self.board[x][y]==p.name:
            if self.board[x][y]==0:
                p.squaresFound+=1
                self.squaresFound+=1
            claimSquare(self,p.name,x,y)
            if self.squaresFound+self.numMines+self.squaresRemoved==self.boardsize*self.boardsize:
                for player in self.playerList:
                    message(player,'Game over. Your score was '+str(player.squaresFound))
        else:
            p.send((str(x)+'\n'+str(y)+'\no'+self.board[x][y]).encode())
    def initSelection(self,p,x,y):
        if self.board[x][y]==1 or self.board[x][y]==0:
                for i in range(x-1,x+2):
                    if i>=0 and i<=self.boardsize:
                        for j in range(y-1,y+2):
                            if j>=0 and j<self.boardsize:
                                if self.board[i][j]==1:
                                    self.board[i][j]=0
                                    self.numMines-=1
                self.board[x][y]=p.name
                p.squaresFound+=1
                self.squaresFound+=1
                p.started=True
                p.startM=str(x)+'\n'+str(y)+'\n'
                for player in self.playerList:
                    player.send((p.startM+'o'+p.name).encode())
                self.started=True
                for player in self.playerList:
                    if not player.started:
                        self.started=False
                if self.started:
                    for player in self.playerList:
                        player.send((player.startM+'c'+'0').encode())
    g = game(addPlayer, process)
    g.started=False
    g.numMines=0
    g.squaresFound=0
    g.squaresRemoved=0
    g.board=[[0]*boardsize for i in range(boardsize)]
    g.boardsize=boardsize
    g.isLegal=isLegal
    g.mineSelect=mineSelect
    for i in range(boardsize):
        for j in range(boardsize):
            if random.random()<pMine:
                g.board[i][j]=1
                g.numMines+=1
    return g
def newGame(data):
    if data[:16]==b'guess the number':
        l=data[16:].split(b'\n')
        print(l)
        lower=int(l[1])
        upper=int(l[2])
        return guessTheNumber(lower, upper)
    if data[:11]==b'minesweeper':
        l=data[11:].split(b'\n')
        boardsize=int(l[1])
        pMine=float(l[2])
        return soloMinesweeper(boardsize,pMine)
    if data[:6]==b'freeze':
        l=data[6:].split(b'\n')
        boardsize=int(l[1])
        pMine=float(l[2])
        g=Minesweeper(boardsize,pMine,freezeLegalMove,freezeMineSelect)
        g.freezeTime=15
        return g
    if data[:6]==b'attack':
        l=data[6:].split(b'\n')
        boardsize=int(l[1])
        pMine=float(l[2])
        g=Minesweeper(boardsize,pMine,attackLegalMove,attackMineSelect)
        g.pMine=pMine
        return g
    if data[:11]==b'area attack':
        l=data[11:].split(b'\n')
        boardsize=int(l[1])
        pMine=float(l[2])
        g=Minesweeper(boardsize,pMine,areaAttackLegalMove,areaAttackMineSelect)
        g.pMine=pMine
        g.freezeTime=15
        g.stage=0
        return g
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#addr='192.168.124.118'
#addr='192.168.162.118'
#s.bind(('10.144.119.197',80))
#s.bind(('192.168.1.240',8000))
addr='localhost'
#addr='0.0.0.0'
#addr = '192.168.1.240'
s.bind((addr,8000))
#t.bind((addr,80))
#s.bind(('172.20.10.2',8000))
s.listen()
s.setblocking(False)
#t.listen()
#t.setblocking(False)
games = {}
cList=[]
waitroom=[]
pList=[]
while True:
    try:
        (connection,address)=s.accept()
        connection.setblocking(False)
        cList.append(connection)
    except BlockingIOError:
        pass
    for c in cList:
        try:
            code=c.recv(1)
            print(code)
            if code==b'l':
                cList.remove(c)
                c=lengthPlayer(c)
                waitroom.append(c)
            if code==b'G':
                handshake=c.recv(1000)
                print(handshake.decode())
                cList.remove(c)
                c=websocketPlayer(c,handshake)
                print('ws')
                waitroom.append(c)
            c.send(b'Send your name.')
        except BlockingIOError:
            pass
        except KeyError as k:
            print(k)
    for p in waitroom:
        try:
            name=p.receive()
            if name:
                print(name)
                name=name.decode()
                if '\n' in name:
                    p.send(b'Names cannot contain newlines.')
                else:
                    p.name=name
                    waitroom.remove(p)
                    pList.append(p)
        except BlockingIOError:
            pass
        except:
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
                if code==110:
                    l=msg.split(b'\n',1)
                    print(l)
                    name=l[0].decode()
                    data=l[1]
                    if name in games:
                        p.send(b'This name is already in use.')
                    else:
                        games[name]=newGame(data)
                if code==106:
                    name=msg.decode()
                    if games[name].addPlayer(p):
                        pList.remove(p)
                    else:
                        p.send(b'Rejected from game')
                if code==103:
                    bl=b''
                    for name in games:
                        bl+=name.encode()+b'\n'
                    bl=bl[:-1]
                    p.send(bl)
        except BlockingIOError:
            pass
        except:
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
                print(e)
                games[g].playerList.remove(p)
                if len(games[g].playerList)==0:
                    deleted.append(g)
    for g in deleted:
        del games[g]
