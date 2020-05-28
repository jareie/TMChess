
import random
import chess.syzygy
import chess.pgn
import chess
import csv
pieces = ["N","n","P","p","R","r","B","b","Q","q"]


#DEFAULT READ FILE datalich.pgn
#default output file DataFEN

#number off pieces
piecesnr = 5

#how many lines you want to iterate, default high so it goes through entire input file

linesIterate = 100000000

# append = true if you want to append to file and keep existing elements in datafen. otherwise false
# and it overwrites the old datafen

append = False




print("Starting game file iteration")


mulbrett =[]
'''
for i in range(1000000):
    brett = genboard(i+20)
    ordet = gentext(brett)
    mulbrett.append(ordet[0])
    print(ordet[0])
'''
boards =[]

pgn = open("data/datalich.pgn")

bigc = 0



while True:

    counter = piecesnr
    
    gameone = chess.pgn.read_game(pgn)
    
    if(gameone is None):

        break
    
    board = gameone.board()
    for move in gameone.mainline_moves():
        
        me = board.piece_map()
        counter = 0
        
        for x in me:
            counter =counter +1
           
            
            
        
        if(counter<piecesnr+1):
            break
        board.push(move)
    
    if(counter<piecesnr+1):
        mulbrett.append(board.fen())
          
    bigc= bigc +1
    
    if(bigc>linesIterate):
        print("done with specified amount of lines")
        break

print("done with game file iteration")
print("starting validation checking, and probing for result")

mulbrett = list(set(mulbrett))
with chess.syzygy.open_tablebase("data/syzygy/datasyz") as tablebase:
    for i in mulbrett:
        print(i)
        
        if(chess.Board(i).is_valid()):
            boardsy = chess.Board(i)
            boards.append([i,str(tablebase.probe_wdl(boardsy))])
            print(str(i) + " :hahahah " + str(tablebase.probe_wdl(boardsy)))
print("done with probing results")

if(append):
    with open('DataFEN.csv', 'a+', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("appending to file")
        
        for i in boards:
            writer.writerow(i)
else:
    with open('DataFEN.csv', 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("writing to file")
        q =["Board","Result"]
        writer.writerow(q)
        for i in boards:
            writer.writerow(i)          

print("done writing to file")



# below is just old random functions, not part of the current generation of data.

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