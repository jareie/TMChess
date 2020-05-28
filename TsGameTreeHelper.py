import Workers
import chess
#from copy import deepcopy
cores = 10

def NextThing(moves):
    nextMoves = []
    #print(moves)
    for i in moves:
        #print(i)
        parent = chess.Board(i)
        #print("--------------------")
        #print(parent.turn)
        for move in parent.legal_moves:
            #child = deepcopy(parent)
            parent.push(move)
            
            #print((move, child.fen()))
            nextMoves.append(parent.fen())
            parent.pop()

    return nextMoves

def MultiTree(inp):
    nextMoves = []
    start_move = inp[0]
    parent = chess.Board(start_move[1])
    for move in parent.legal_moves:
        #child = deepcopy(parent)
        parent.push(move)
        nextMoves.append(parent.fen())
        parent.pop()
    
    #final = 
    depth = inp[1]-2
    #print(depth)
    if depth <= 0:
        return [(start_move[0], mv) for mv in nextMoves]
    
    final = nextMoves
    for i in range(depth):
        final = NextThing(final)
    #print(len(final))
    return [(start_move[0], mv) for mv in final]


def GetMoves(cur_moves, depth):
    temp = [(i, depth) for i in cur_moves]
    #print("Hello there")
    #print(temp)
    temp_move_list = Workers.MakeWorkers(MultiTree, temp, cores)
    #print(temp_move_list)
    moves = []
    for i in temp_move_list:
        moves.extend(i)
    return moves


def MultiScore(movs):
    moves = movs[0]
    machine = movs[1]()
    results = []
    #print("Hello", len(moves))
    for i in moves:
        results.append((i[0], machine.Predict(i[1])))
    #print("Finished")
    return results


def Scorer(moves, machine):
    workloads = []
    
    partition = len(moves)/cores
    for i in range(cores):
        workloads.append((moves[int(i*partition):int((i+1)*partition)], machine))
    #print(workloads)
    #print("Scoring", len(workloads))
    scores = Workers.MakeWorkers(MultiScore, workloads, cores)
    #print("Scoring Finished")
    final = []
    
    for i in scores:
        final.extend(i)
    return final

def TreeScorer(inp):
    move = inp[0]
    machine = inp[1]()
    depth = inp[2]

    final = [move[1]]
    for i in range(depth):
        prev = final
        final = NextThing(final)

    results = []
    #print("Hello", len(moves))
    #print(final)
    if len(final) < 1:
        #print(move[1])
        prd = machine.Predict(move[1])
        if prd[0] == 1:
            return [move[0], 1]
        else:
            return [move[0], 0]
    
    for i in final:
        #print()
        results.append(machine.Predict(i))

    predictions = [0,0,0]

    #print(results)
    for i in results:
        predictions[i[0]] += 1

    score = predictions[1]/len(results)

    return [move[0], score]

def TreeScore(move, machine, depth):
    moves = [(i, machine, depth) for i in move]

    scores = Workers.MakeWorkers(TreeScorer, moves, cores)

    return scores


