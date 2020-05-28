try:
    import pyspiel
except ImportError:
    print("Use virtual environment to use PySpiel")

#print(game)

from TsetlinMachineScripts import ChessTM
from TsetlinMachineScripts import gennextmove
from TsetlinMachineScripts import Translator
import numpy as np


#fen_board = "3K4/2P5/8/8/8/8/8/3k4 w - - 0 1"
#fen_board = "2k5/8/6R1/KP6/8/5r2/8/8 w - - 0 75"
fen_board = "8/8/8/4QK2/8/2nkp3/8/8 w - - 0 56"

#ChessTM.NonConvolutionalTrain()
#ChessTM.RevConvolutionalLoad("Machine")
TsetlinMachine = ChessTM.ClassesSplit()
#TsetlinMachine.TrainMachine(50)
#TsetlinMachine.SaveMachine("SplitMachine1")
TsetlinMachine.LoadMachine("SplitMachine1")
#TsetlinMachine.RevConvolutionalLoad("RevConv1")
#OldTM = ChessTM.Machine[0]
#OldTM.SaveMachine("Machine")

moves_done = []

def SortValue(inp):
    #Get the scoring for the prediction
    #Which move it prefers
    return inp[2]

game = pyspiel.load_game("chess")

count = 0
amount_moves = 2


    