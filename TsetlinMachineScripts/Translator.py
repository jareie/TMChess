def IsNumber(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def Return7Bits(typeOfPiece, white, reversePlayerColour):
    if white:
        if reversePlayerColour:
            return [0] + typeOfPiece
        else:
            return [1] + typeOfPiece
    else:
        if reversePlayerColour:
            return [1] + typeOfPiece
        else:
            return [0] + typeOfPiece

def Return12Bits(typeOfPiece, white, reversePlayerColour):
    if white:
        if reversePlayerColour:
            return [0 for i in range(6)] + typeOfPiece
        else:
            return typeOfPiece + [0 for i in range(6)]
    else:
        if reversePlayerColour:
            return typeOfPiece + [0 for i in range(6)]
        else:
            return [0 for i in range(6)] + typeOfPiece


def CreatePiece(piece, numberOfBits=7, reversePlayerColour=False):
    pieces = ["P","B","N","R","Q","K"]
    typeOfPiece = [0 for i in range(len(pieces))]
    white = True
    CopyPiece = piece.upper()

    if piece.islower():
        white = False
    
    if not CopyPiece in pieces:
        if numberOfBits == 12:
            return typeOfPiece + [0 for i in range(6)]

        return [0] + typeOfPiece

    for i in range(len(pieces)):
        if pieces[i] == CopyPiece:
            typeOfPiece[i] = 1
            break

    if numberOfBits == 12:
        return Return12Bits(typeOfPiece, white, reversePlayerColour)
    #1 = white, 0 = black

    return Return7Bits(typeOfPiece, white, reversePlayerColour)
    

# Turns a board off FEN standard, into a board of bits
# FENBoard is the board to change
# Number of Bits is the representation of a square on the board
# Reverse player colour is if the colour of the pieces on the board should be reversed
# startingplayerReverse changes the pieces for a given player
def FENtoBits(FENBoard, numberOfBits=7, reversePlayerColour=False, startingPlayerReverse="b",startingplayerbits=False):
    #print("Hello:",FENBoard)
    available_bits = [7,12]
    if not numberOfBits in available_bits:
        raise Exception("Only the specified values are allowed for numberOfBits:",available_bits)
    
    BitBoard = []
    cleaning = FENBoard.split(" ")[:2]   
    board = cleaning[0].split("/")

    reverseBoard = False
    try:
        if reversePlayerColour and startingPlayerReverse == cleaning[1]:
            reverseBoard = True
    except:
        print(FENBoard, cleaning)
    

    for row in board:
        #print(row)
        newRow = []
        for FENPiece in row:
            if IsNumber(FENPiece):
                for piece in range(int(FENPiece)):
                    piece = CreatePiece("", numberOfBits, reverseBoard)
                    newRow.extend(piece)
            else:
                piece = CreatePiece(FENPiece, numberOfBits, reverseBoard)
                newRow.extend(piece)
        BitBoard.extend(newRow)

    if reverseBoard:
        reverse_board = []
        import numpy as np
        t = np.array(BitBoard)
        t = np.reshape(t,(8,8,numberOfBits))

        BitBoard = np.flip(t,(0,1)).reshape((8*8*numberOfBits)).tolist()

        #BitBoard = reverse_board
    if startingplayerbits:
        if cleaning[1] == "w":
            return BitBoard + [0 for i in range(len(BitBoard))]
        else:
            return [0 for i in range(len(BitBoard))] + BitBoard
    else:
        return BitBoard

def FENtoBitsWStartingPlayer(FENBoard, numberOfBits=7):
    cleaning = FENBoard.split(" ")[:2]
    BitBoard = FENtoBits(FENBoard, numberOfBits)

    def StringTooBitStartPlayer(inp):
        if inp == "w":
            return 1
        else:
            return 0
    #print(cleaning[1])
    startingPlayer = StringTooBitStartPlayer(cleaning[1])
    return BitBoard + [startingPlayer]

#bo = FENtoBitsWStartingPlayer("8/3k4/3n4/8/8/K7/8/8 w - - 0 1")
