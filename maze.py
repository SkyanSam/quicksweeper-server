import random
def main(boardsize):
    board=[[0]*(boardsize+1) for i in range(boardsize+1)]
    infinity=2**30
    def potential(x,y):
        res=0
        for i in range(boardsize+1):
            for j in range(boardsize+1):
                if i==x and j==y:
                    if board[x][y]==1:
                        return infinity
                else :
                    res+=board[i][j]*1/((x-i)**2+(y-j)**2)
        return res
    l=[]
    destroyThreshold=6
    createThreshold=3
    def process():
        for k in range(len(l)-1,-1,-1):
            j=l[k]
            x=j[0]
            y=j[1]
            baseline=potential(x,y)
            if baseline>destroyThreshold and baseline!=infinity:
                l.remove(j)
                continue
            if baseline<createThreshold:
                l.append([x,y])
            t=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
            s=[]
            total=0
            for i in t:
                total+=max(baseline-potential(i[0],i[1]),0)
            if total==0:
                l.remove(j)
            else:
                for i in t:
                    for h in range(int(32*(baseline-potential(i[0],i[1]))/total)):
                        s.append(i)
                board[x][y]=1
                new=random.choice(s)
                j[0]=new[0]
                j[1]=new[1]
    for i in range(boardsize+1):
        board[0][i]=1
        board[boardsize][i]=1
        board[i][0]=1
        board[i][boardsize]=1
    spacing = 10
    for i in range(1,boardsize//spacing):
        for j in range(1,boardsize//spacing):
            l.append([i*spacing,j*spacing])
            board[i*spacing][j*spacing]=1
    while len(l)>0:
        process()
    return board
