
import random
import chess.syzygy
import chess.pgn
import chess
import csv

pieces = ["N","n","P","p","R","r","B","b","Q","q"]
def gentext(board):
    positioncounter = 0
    actioncounter = 0
    word = ""
    for i in range(0, 8):
        for j in range(0, 8):
            
            if(board[positioncounter]==0):
                actioncounter = actioncounter+1
            else:
                if(actioncounter!=0):
                    word = word+ str(actioncounter)
                word = word + board[positioncounter]
                actioncounter= 0
            if (j==7):
                if(board[positioncounter]==0):
                    
                    word = word+ str(actioncounter)
                if(i!=7):
                    word = word + "/"
                actioncounter= 0
               
            positioncounter = positioncounter+1
    wordw = word +" w - - 0 1"
    wordb = word +" b - - 0 1"
    return [wordw,wordb]
    



def genboard(seed):
    boardgenerated =[]
    for i in range(64):  
        boardgenerated.append(0)
    random.seed(seed)
    if(random.randint(0,50)>40):
        king1, king2, extra1 = random.sample(range(0,63),3)
        extra1s = pieces[random.randint(0,9)]
        boardgenerated[int(king1)] = "K"
        boardgenerated[int(king2)] = "k"
        boardgenerated[int(extra1)] = extra1s
    elif(random.randint(0,50)>30):
        king1, king2, extra1, extra2 = random.sample(range(0,63),4)
        extra1s = pieces[random.randint(0,9)]
        random.seed(seed+1)
        extra2s = pieces[random.randint(0,9)]
        boardgenerated[int(king1)] = "K"
        boardgenerated[int(king2)] = "k"
        boardgenerated[int(extra1)] = extra1s
        boardgenerated[int(extra2)] = extra2s
    else:
        king1, king2, extra1, extra2, extra3 = random.sample(range(0,63),5)
        extra1s = pieces[random.randint(0,9)]
        random.seed(seed+1)
        extra2s = pieces[random.randint(0,9)]
        random.seed(seed+1)
        extra3s = pieces[random.randint(0,9)]
        boardgenerated[int(king1)] = "K"
        boardgenerated[int(king2)] = "k"
        boardgenerated[int(extra1)] = extra1s
        boardgenerated[int(extra2)] = extra2s
        boardgenerated[int(extra3)] = extra3s


    return boardgenerated
mulbrett =[]
boards =[]
brett = genboard(300)
ordet = gentext(brett)
#print(ordet)
#mulbrett.append(ordet[0])
#mulbrett.append(ordet[1])
'''
for i in range(1000000):
    brett = genboard(i+20)
    ordet = gentext(brett)
    mulbrett.append(ordet[0])
    print(ordet[0])
'''
ordo = "B7/8/6K1/7B/1B6/8/8/5k2 w - - 0 1"
ordone = "b7/8/6k1/7b/1b6/8/8/5K2 w - - 0 1"
mulbrett.append(ordo)
mulbrett.append(ordone)
mulbrett = list(set(mulbrett))
with chess.syzygy.open_tablebase("data/syzygy/datasyz") as tablebase:
    for i in mulbrett:
        print(i)
        
        if(chess.Board(i).is_valid()):
            boardsy = chess.Board(i)
            boards.append([i,str(tablebase.probe_wdl(boardsy))])
            print(str(i) + " :hahahah " + str(tablebase.probe_wdl(boardsy)))
