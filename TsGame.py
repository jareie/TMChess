'''
try:
    import pyspiel
except ImportError:
    print("Use virtual environment to use PySpiel")
'''

#game = pyspiel.load_game("chess")
#print(game)
#from mem_top import mem_top

#import gc

import chess

import numpy as np
#from copy import deepcopy

def probe(game):
    with chess.syzygy.open_tablebase("Dataset/data/syzygy/regular") as tablebase:
        return tablebase.probe_wdl(game)

class Player:
    def __init__(self):
        self.MakeMove = None

import math
def PlayGame(game_fen, player1, player2, depth, max_moves=math.inf):
    game = chess.Board()
    game.set_fen(game_fen)
    
    def PlayerMove(player):
        #player makes a move
        uci_move = chess.Move.from_uci(player.MakeMove(game.fen(), depth))
        #move = chess.Move.from_uci(uci_move)
        #print(uci_move)
        game.push(uci_move)
        
        #check if game is over
        if game.is_game_over():
            return 1
        return 0

    
    count = 0
    while not game.is_game_over() and count < amount_moves:
        #print(count)
        #print("Player 1 is moving")
        if PlayerMove(player1):
            break
        #print("Player 2 is moving")
        if PlayerMove(player2):
            break
        #print(mem_top())
        #print(gc.get_objects())
        count += 1
    
    if not game.is_game_over():
        #Do some tablebase check in order to see who
        #has the advantage.
        game_res = probe(game)
        #print("Not finished game: ", game_res, game.turn)
        if game_res == 0:
            return (0, 2)
        elif game_res > 0:
            if game.turn:
                return (1, 2)
            else:
                return (2, 2)
        else:
            if game.turn:
                return (2, 2)
            else:
                return (1, 2)
        return (-2, 2)

    res = game.result()
    #print("Hey Hey:", res)
    if res == "1-0":
        #white won
        return (1, 1)
    elif res == "0-1":
        #black won
        return (2, 1)
    elif res == "1/2-1/2":
        #draw
        return (0, 1)
    else:
        #Error
        print(res)
        return (-1, 1)

#Setup opponent
# - Monte Carlo

from mcts import mcts

class ChessMCTS:
    def __init__(self,gameFEN):
        self.player = 1
        self.gameFEN = gameFEN

    def getCurrentPlayer(self):
        return self.player

    def getPossibleActions(self):
        brd = chess.Board(self.gameFEN)
        moves = []
        for i in brd.legal_moves:
            #tempBrd = chess.Board(fen=self.gameFEN)
            #tempBrd.push(i)
            moves.append(Action(self.player, i.uci()))
        return moves

    def takeAction(self, action):
        brd = chess.Board(self.gameFEN)
        brd.push(chess.Move.from_uci(action.move))
        newState = ChessMCTS(brd.fen())
        newState.player = newState.player * -1
        return newState

    def isTerminal(self):
        brd = chess.Board(self.gameFEN)
        if brd.is_game_over():
            return True
        return False

    def getReward(self):
        brd = chess.Board(self.gameFEN)
        if brd.is_variant_win():
            return 1
        elif brd.is_variant_draw():
            return 0
        elif brd.is_variant_loss():
            return -1
        
        return False

class Action:
    def __init__(self,player,move):
        self.player = player
        self.move = move

    def __hash__(self):
        return hash((self.player, self.move))


mcts = mcts(timeLimit=1000)
#mcts = mcts(iterationLimit=1000)

#print(bestAction.move)
def mctsMove(game, depth):
    initialState = ChessMCTS(game)
    move = mcts.search(initialState=initialState).move
    #print(move.move)
    return move

mctsP = Player()
mctsP.MakeMove = mctsMove





# - random
from random import sample
def randEval(game, depth):
    brd = chess.Board(game)
    moves = []
    for i in brd.legal_moves:
        moves.append(i)
    
    return sample(moves,1)[0].uci()
rand = Player()
rand.MakeMove = randEval

#--------------------------------
#Tsetlin Machine setup

from TsetlinMachineScripts import ChessTM
from TsetlinMachineScripts import gennextmove
from TsetlinMachineScripts import Translator
import TsGameTreeHelper
#TsetlinMachine = ChessTM.ClassesSplit()
#TsetlinMachine.TrainMachine(50)
#TsetlinMachine.Save("SplitMachine1")

class TsetlinPlayer:
    def __init__(self, tsm):
        self.tsm = tsm

    def tsmMove(self, game, depth):
        def TsmSortingConfidence(inp):
            prediction = inp[-1]
            scores = prediction[-1]
            #print(scores)
            if scores[0] > 0:
                return scores[0] * scores[1]
            else:
                return scores[0] * scores[1]
        def scortingAmountWin(inp):
            return inp[1]

        moves = []
        #can be changed to do a deeper search
        #For now just the next

        def DepthTree(moves, curDepth=0):
            nextMoves = []
            #print(curDepth)
            #print(moves)
            for i in moves:
                #print(i)
                parent = chess.Board(i[1])
                for move in parent.legal_moves:
                    #child = deepcopy(parent)
                    parent.push(move)
                    #print((move, child.fen()))
                    nextMoves.append((move.uci(), parent.fen()))
                    parent.pop()
            if curDepth >= depth:
                return nextMoves
            
            return DepthTree(nextMoves, curDepth+1)

        tmp_brd = chess.Board(game)
        for i in tmp_brd.legal_moves:
            #child = deepcopy(tmp_brd)
            tmp_brd.push(i)
            moves.append((i.uci(), tmp_brd.fen()))
            tmp_brd.pop()
        
        #moves = DepthTree(moves, 1)
        #moves = TsGameTreeHelper.GetMoves(moves, depth)
        #print(moves)
        #predictions = TsGameTreeHelper.Scorer(moves, self.tsm)
        predictions = TsGameTreeHelper.TreeScore(moves, self.tsm, depth)
        #predictions = []
        '''
        print("Scoring moves")
        predictions = []
        #print(len(moves))
        uci_move = []
        board_fen_scoring = []
        #print(moves)
        for i in moves:
            #print(i, cnt)
            uci_move.append(i[0])
            board_fen_scoring.append(i[1])
            #predictions.append((i[0], self.tsm.Predict(i[1])))
        prd = self.tsm.MassPredict(board_fen_scoring)
        
        predictions = []
        for i in range(len(prd)):
            predictions.append((uci_move[i], prd[i]))
        '''
        #print("Sorting")
        #predictions.sort(key=TsmSortingConfidence,reverse=True)
        predictions.sort(key=scortingAmountWin,reverse=True)

        #print("Sorting done")
        #predictions = predictions[:100]

        #return the move it is the most confident about that is win
        #print("Finding moves")
        #print(predictions)
        return predictions[0][0]
        for i in predictions:
            if i[-1][0] == 1:
                return i[0]
        
        #return the move it thinks is draw
        #backup if it does not find a win
        for i in predictions:
            if i[-1][0] == 2:
                return i[0]

        #return a move, so the game can continue
        for i in predictions[::-1]:
            if i[-1][0] == 0:
                return i[0]

machinepath = "Dataset/data/results/machines/"
paral = False
#======================
#==  
#======================
def tsmFp3M():
    Tsm1 = ChessTM.RevConvolutional()
    Tsm1.parallel = paral
    Tsm1.Load(machinepath + "3pieces-3x3")
    return Tsm1

Tsmm1 = TsetlinPlayer(tsmFp3M)
tsmFp3 = Player()
tsmFp3.MakeMove = Tsmm1.tsmMove

#======================
#==  
#======================
def tsmFp4M():
    Tsm2 = ChessTM.RevConvolutional()
    Tsm2.parallel = paral
    Tsm2.double_bits = True
    Tsm2.Load(machinepath + "4pieces-5x5-BitsTest")
    return Tsm2

Tsmm2 = TsetlinPlayer(tsmFp4M)
tsmFp4 = Player()
tsmFp4.MakeMove = Tsmm2.tsmMove


#======================
#==  
#======================
def tsmSp4M():
    Tsm3 = ChessTM.SideSplit()
    Tsm3.parallel = paral
    Tsm3.double_bits = True
    Tsm3.Load(machinepath + "4pieces-5x5-BitsTest")
    return Tsm3

Tsmm3 = TsetlinPlayer(tsmSp4M)
tsmSp4 = Player()
tsmSp4.MakeMove = Tsmm3.tsmMove


#fen_board = "3K4/2P5/8/8/8/8/8/3k4 w - - 0 1"
#fen_board = "2k5/8/6R1/KP6/8/5r2/8/8 w - - 0 75"

#Game parameters
amount_moves = 50


def TestingGames(game, mainAlgorithm, opponent, amount, depth):
    res_games = []
    starting_player = 1
    if game.find("w") < 0:
        starting_player = 2

    for i in range(amount):
        print(i)
        game_res = PlayGame(fen_board, mainAlgorithm, opponent, depth, amount_moves)
        #print(game_res)
        if starting_player == game_res[0]:
            #win
            res_games.append((1, game_res[1]))
        elif game_res[0] == 0:
            #draw
            res_games.append((0, game_res[1]))
        else:
            #loss
            res_games.append((-1, game_res[1]))
    
    for i in range(amount):
        print(i+amount)
        game_res = PlayGame(fen_board, mainAlgorithm, opponent, depth, amount_moves)
        #print(game_res)
        if game_res[0] == 0:
            #draw
            res_games.append((0, game_res[1]))
        elif starting_player == game_res[0]:
            #loss
            res_games.append((-1, game_res[1]))
        else:
            #win
            res_games.append((1, game_res[1]))
    return (starting_player, res_games)

fen_board = "8/8/8/4QK2/8/2nkp3/8/8 w - - 0 56"


pairings = [
    (tsmFp4, rand),
    (tsmFp4, mctsP),
    (tsmFp4, tsmFp3),
    (tsmFp4, tsmSp4),

    (tsmFp3, rand),
    (tsmFp3, mctsP),
    (tsmFp3, tsmSp4),

    (tsmSp4, rand),
    (tsmSp4, mctsP)
]

#pairings = [(tsmFp4, rand)]
#pairings = [(tsmFp4, mctsP)]
#pairings = [(tsmFp4, tsmFp3)]
#pairings = [(tsmFp4, tsmSp4)]
#pairings = [(tsmFp3, rand)]
#pairings = [(tsmFp3, mctsP)]
#pairings = [(tsmFp3, tsmFp4)]
#pairings = [(tsmFp3, tsmSp4)]
#pairings = [(tsmSp4, rand)]
#pairings = [(tsmSp4, mctsP)]
#pairings = [(tsmSp4, tsmFp3)]
#pairings = [(tsmSp4, tsmFp4)]



replay_game = 10
depth = 3

res_file = open("resFile_Scoring_amount_win_tsGame.txt","a")
#res_file = open("resFile_tsGame.txt","a")
res_file.write("1 means white as starting side, 2 means black\n")
res_file.write("Depth: " + str(depth) + "\n\n")

'''def multi(pairing):
    return TestingGames(fen_board, pairing[0], pairing[1], replay_game)

scor = MakeWorkers(multi, pairings, 6)
for i in scor:
    res_file.write("Player starting as: " + str(res[0]) + ", Result: " + str(res[1]) + "\n")
'''

for i in range(len(pairings)):
    print("Doing pairing: " + str(i))
    res = TestingGames(fen_board, pairings[i][0], pairings[i][1], replay_game, depth)
    res_file.write("Player starting as: " + str(res[0]) + ", Result: " + str(res[1]) + "\n")

res_file.write("\n")
res_file.close()
#print(TestingGames(fen_board, tsmP, mctsP, 50))
