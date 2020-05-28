import chess
import os
import chess.pgn
import chess.syzygy
import GenRandomData as GRD


def GetNextSetOfMoves(Fen, earlier_moves):
    board = chess.Board(Fen)
    legalmoves = []
    with chess.syzygy.open_tablebase("Dataset/data/syzygy/regular") as tablebase:
        for move in board.legal_moves:
            board.push(move)
            legalmoves.append([earlier_moves + [move.uci()], board.fen(), tablebase.probe_wdl(board)])
            board.pop()
    return legalmoves

def FindLeafNodes(game_fen, max_depth):
    game = chess.Board(game_fen)
    
    def NextLevel(move, depth):
        newgame = chess.Board(move[1])
        
        #Check if the game is over
        # then evaluate who won and
        # who we are evaluating from
        if newgame.is_game_over():
            result = newgame.result()
            if result == "1-0":
                if game.turn == chess.WHITE:
                    return [move[:-1] + [1]]
                else:
                    return [move[:-1] + [-1]]
            elif result == "0-1":
                if game.turn == chess.BLACK:
                    return [move[:-1] + [1]]
                else:
                    return [move[:-1] + [-1]]
            else:
                return [move[:-1] + [0]]
        
        moves = GetNextSetOfMoves(move[1], move[0])
        if depth >= max_depth:
            return moves
        
        nodes = []
        for i in moves:
            nodes.extend(NextLevel(i, depth+1))
        
        return nodes
    
    return NextLevel([[],game_fen,0],0)

def FilesInDir(dirPath):
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]
    return files

def MakeDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def GenerateGames(path="Dataset/data/TreeSearch", games=100, depth=3, seed=0):
    MakeDirectory(path)
    Files = FilesInDir(path)

    for i in range(games):
        game_fen = GRD.genboard(seed=seed+i)
        bb = chess.Board(game_fen).is_valid()
        
        while (game_fen in Files) or not bb:
            game_fen = GRD.genboard()
            bb = chess.Board(game_fen).is_valid()
        
        leaf_nodes = FindLeafNodes(game_fen, depth-1)
        cur_path = path + "/" + game_fen.replace("/",",")

        
        '''state_file = open(cur_path + ".csv","w", newline='', encoding='utf-8')
        for node in leaf_nodes:
            name = ""
            for move in node[0]:
                name += move + "|"
            
            final = name + ", " + node[1] + ", " + str(node[2]) + "\n"
            #print(node, final)
            state_file.write(final)
        state_file.close()'''

        import csv
        with open(cur_path + ".csv","w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(["Board","Result"])
            for node in leaf_nodes:
                writer.writerow([node[1], node[2]])

        Files.append(cur_path + ".csv")

if __name__ == "__main__":
    GenerateGames()