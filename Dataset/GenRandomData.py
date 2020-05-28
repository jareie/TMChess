import random

def gentext(board):
    positioncounter = 0
    actioncounter = 0
    word = ""
    Bord = []
    for i in range(0, 8):
        posStart = i*8
        posEnd = (i+1)*8
        CurBoard = board[posStart:posEnd]
        row = ""
        counter = 0
        
        for part in range(len(CurBoard)):
            if CurBoard[part] != 0:
                if counter == 0:
                    row += CurBoard[part]
                else:
                    row += str(counter) + CurBoard[part]
                counter = 0
                continue
            counter += 1
        
        if counter > 0:
            row += str(counter)
        Bord.append(row)
    
    
    word += Bord[0]
    for i in Bord[1:]:
        word += "/" + i


    '''for i in range(0, 8):
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
    '''
    wordw = word +" w - - 0 1"
    wordb = word +" b - - 0 1"
    return [wordw, wordb]

#typeRet is: 0=random, 1=white, 2=black, 3=both
def genboard(amount_pieces=5, typeRet=0, seed=None):
    random.seed(seed)

    def generateBoard():
        boardgenerated = []
        pieces = ["N","N","n","n","P","P","p","p","R","R","r","r","B","B","b","b","Q","q"]
        #length_pieces = len(pieces)-1
        
        for i in range(64):  
            boardgenerated.append(0)
        
        kingW, kingB = random.sample(range(0,63),2)
        #print("Kings:",kingW,kingB)
        boardgenerated[int(kingW)] = "K"
        boardgenerated[int(kingB)] = "k"
        
        #print("amount_pieces:",amount_pieces)
        for i in range(amount_pieces-2):
            piece_index = random.randint(0,63)
            
            while not boardgenerated[piece_index] == 0:
                piece_index = random.randint(0,63)
            #print(piece_index,boardgenerated[piece_index])
            
            #print("Pieces left:",len(pieces))
            piece_type = random.randint(0,len(pieces)-1)
            #print(piece_index)
            #length_pieces -= 1
            
            piece = pieces.pop(piece_type)
            boardgenerated[piece_index] = piece

        return boardgenerated
    
    
    b = generateBoard()
    #print(b)
    
    FEN = gentext(b)

    random.seed(None)
    
    if typeRet == 0:
        return FEN[random.randint(0,1)]
    elif typeRet == 1:
        return FEN[0]
    elif typeRet == 2:
        return FEN[1]
    else:
        return FEN
    

def genMultipleBoards(amount,amount_pieces=5,typeRet=0,seed=None):
    boards = []
    for i in range(amount):
        boards.append(genboard(amount_pieces,typeRet,seed))
    return boards