import os
import chess.pgn
import chess.syzygy

#print()
def CreateTopPlayerData(FileName):
    Directories = os.listdir("data/Raw_game/")
    data = []
    BoardsForData = []

    for i in Directories:
        Files = os.listdir("data/Raw_game/" + i + "/")
        for game in Files:
            oneGame = chess.pgn.read_game(open("data/Raw_game/" + i + "/" + game))
            data.append(oneGame)

    with chess.syzygy.open_tablebase("data/syzygy/regular") as tablebase:
        for game in data:
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
                amountOfPieces = len(board.piece_map())
                if amountOfPieces < 6:
                    BoardsForData.append([board.fen(),str(tablebase.probe_wdl(board))])

    writemode = 'w'
    FileExists = os.path.exists(FileName)

    if FileExists:
        writemode = 'a'

    import csv
    with open(FileName, writemode, newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if not FileExists:
            writer.writerow(['Board', 'Result'])
        
        for i in BoardsForData:
            writer.writerow(i)

CreateTopPlayerData("Top10.csv")
#open("data/Raw_game/")