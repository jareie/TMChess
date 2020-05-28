from TsetlinMachineScripts import ChessTM
from TsetlinMachineScripts import Translator
from TsetlinMachineScripts import gennextmove
import Workers as W
import csv

def GetWinLossDraw(inp):
    if inp < 0:
        return 0
    elif inp > 0:
        return 1
    else:
        return 2

def ScorePlay(nodes,Tm):
    print("Scoring")
    percent_complete = 0.0

    '''
    def SortPreds(inp):
        scores = inp[-1]
        #print(scores)
        if scores[0] > 0:
            return scores[0] * scores[1]
        else:
            return scores[0] * (1 + scores[1])'''
    
    def SortPreds(inp):
        scores = inp[-1]
        return scores[0] * scores[1]

    predictions = []
    #score = 0.0
    for i in nodes:
        pred = Tm.Predict(i[0])
        predictions.append([GetWinLossDraw(i[1])] + pred)   
    predictions.sort(key=SortPreds,reverse=True)
    #nodes.sort(key=SortScore,reverse=True)
    return predictions

def recall(games, amount):
    all_rcl_results = []
    for rcl in range(amount):
        rcl_results = [[0,0,0] for i in range(3)]
        #print("Amount: ", len(games[:rcl]))
        rcl_games = []
        for game in games:
            rcl_games.extend(game[:rcl+1])

        for pred in rcl_games:
            rcl_results[pred[0]][pred[1]] += 1
        all_rcl_results.append(rcl_results)
    return all_rcl_results
        


def FilesInDir(dirPath):
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]
    return files

def Machines(inp):
    double_bits = False
    if inp.find("-BitsTest") > -1 or inp.find("-bitsTest") > -1:
        double_bits = True
    if inp.find("-Win.json") > -1 or inp.find("-Other.json") > -1:
        TsmTemp = ChessTM.ClassesSplit()
        TsmTemp.parallel = False
        TsmTemp.double_bits = double_bits
        TsmTemp.Load(inp.replace("-Win.json","").replace("-Other.json",""))
        return TsmTemp
    elif inp.find("-white.json") > -1 or inp.find("-black.json") > -1:
        TsmTemp = ChessTM.SideSplit()
        TsmTemp.parallel = False
        #TsmTemp.double_bits = double_bits
        TsmTemp.Load(inp.replace("-white.json","").replace("-black.json",""))
        return TsmTemp

    elif inp.find("-rev.json") > -1:
        TsmTemp = ChessTM.RevConvolutional()
        TsmTemp.parallel = False
        TsmTemp.double_bits = double_bits
        TsmTemp.Load(inp.replace("-rev.json",""))
        return TsmTemp

    elif inp.find("-conv.json") > -1:
        TsmTemp = ChessTM.Convolutional()
        TsmTemp.parallel = False
        TsmTemp.double_bits = double_bits
        TsmTemp.Load(inp.replace("-conv.json",""))
        return TsmTemp

    elif inp.find("-NonConv.json") > -1:
        TsmTemp = ChessTM.NonConvolutional()
        TsmTemp.parallel = False
        TsmTemp.double_bits = double_bits
        TsmTemp.Load(inp.replace("-NonConv.json",""))
        return TsmTemp


#print("Leaf Nodes generated")
#machine_name = "SplitMachine1"
#machine_names = ["3pieces-7x7-BitsTest-Win.json","3pieces-3x3-white.json","3pieces-3x3-rev.json"]
#machine_names =["4pieces-5x5-BitsTest-white.json","4pieces-5x5-BitsTest-Win.json","4pieces-5x5-BitsTest-rev.json"]
machine_names =["5pieces-2x2-white.json", "5pieces-5x5-bitsTest-Win.json", "5pieces-2x2-rev.json"]

#machine_names = ["allpieces-5x5_split_0-rev.json","4pieces-2x2_split_0-rev.json","4pieces-5x5-BitsTest-noDraw_split_0-rev.json","4pieces-5x5-BitsTest-noDraw_split_0-white.json"]
#machine_names = ["4pieces-5x5-BitsTest-noDraw_split_0-white.json"]
machine_path = "Dataset/data/results/machines"

#Load files for recall
path = "Dataset/data/TreeSearch"
#save path
save_path = "Dataset/data/results/treesearch"
amount_highest_score = 100
final_score = 0


Files = FilesInDir(path)

def MultiScoring(machine_and_file):
    #print("Hello")
    machine = Machines(machine_path + "/" + machine_and_file[0])
    #machine = machine_and_file[0]
    state_file = machine_and_file[1]
    
    nodes = []
    with open(path + "/" + state_file,"r",newline="",encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            nodes.append(row)
        nodes =[[i[0],int(i[1])] for i in nodes[1:]]
        #print(nodes[0])

    #nodes = ScorePlay(nodes,Tsm)
    #print(nodes)
    #return recall(nodes, amount_highest_score)
    return ScorePlay(nodes, machine)

def GetResults(m_names):
    def scoreMachine(machineName):
        multi_data = [(machineName, i) for i in Files]
        #print(multi_data)
        scores = W.MakeWorkers(MultiScoring, multi_data, 10)
        #scores = []
        #for i in multi_data:
        #    scores.append(MultiScoring(i))


        #print(path + "/results/" + machine.replace(".json","") + ".txt")
        recall_file = open(path + "/results/" + machineName.replace(".json","") + "_orgScore.txt","w")
        for i in range(len(scores)):
            res = scores[i]
            string = ""
            for scr in res:
                string += str(scr[0]) + " - " + str(scr[1]) + ", "
            string += "\n"
            recall_file.write(string)
        recall_file.close()

    for machine in machine_names:
        scoreMachine(machine)
    #W.MakeWorkers(scoreMachine, m_names, 10)


GetResults(machine_names)