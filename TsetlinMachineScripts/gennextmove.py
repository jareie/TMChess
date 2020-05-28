import os
import chess.pgn
import chess.syzygy

#print()
def CreateTopPlayerData(Fen):
    board = chess.Board(Fen)
    legalmoves = []
    with chess.syzygy.open_tablebase("Dataset/data/syzygy/regular") as tablebase:
        for move in board.legal_moves:
            board.push(move)
            legalmoves.append([move.uci(), board.fen(), tablebase.probe_wdl(board)])
            board.pop()
    return legalmoves

#arrays = CreateTopPlayerData("3K4/2P5/8/8/8/8/8/3k4 w - - 0 1")

#print(arrays)
#open("data/Raw_game/")