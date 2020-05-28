import numpy as np
import matplotlib.pyplot as plt

res_dir = "TreeSearch/results"

def FilesInDir(dirPath):
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]
    return files

results = FilesInDir(res_dir)

recall = 100

games_score = []
for res_file in results:
    print(res_file)
    scores = [i.replace("\n","").replace(" ","").split(",")[:recall] for i in open(res_dir + "/" + res_file,"r").readlines()]
    games_score.append(scores)
    #print(scores)
    #break


def ClacGame(game_score):
    final_scores = []
    
    for number in range(recall):
        scores = [[0,0,0] for i in range(3)]
        for game in game_score:
            #print(game)
            for i in game[:number+1]:
                if i == "":
                    continue
                temp = i.split("-")
                #print(temp)
                scores[int(temp[0])][int(temp[-1])] += 1
        final_scores.append(scores)

    #print(final_scores)
    #print("------------------------")
    graph_res = []
    graph_precision = []
    for i in final_scores:
        #sum(i[1]) = np.sum(np.array(i[1]))
        #print(i[1], i[1][1])
        tot = 0
        for number in i[1]:
            tot += number

        graph_res.append(i[1][1]/tot)

        totPrec = 0
        for number in i:
            totPrec += number[1]
        prec = i[1][1]/totPrec
        graph_precision.append(prec)
    return [graph_res, graph_precision]
    
maxRes = open("Treesearch_average_recall_and_amount_of_moves.txt","w")
for game in range(len(games_score)):
    res = ClacGame(games_score[game])
    plt.clf()
    plt.plot(res[0], label="Recall")
    plt.plot(res[1], label="Precision")
    #plt.ylim(0,100)
    plt.xlabel("Amount of moves per game")
    plt.ylabel("Percent")
    name = results[game].replace(".txt","").replace("_orgScore","").replace("BitsTest","Moving player bits").replace("-rev"," Flipped Player").replace("-white"," Moving Player").replace("-black"," Moving Player").replace("-Win"," Split Result").replace("-Other"," Split Result").replace("-"," ").replace(" Result","")
    plt.title(name)
    plt.legend()
    #plt.show()
    #print(name)
    #print(results[game])
    maxRes.write(name + "     " + results[game] + "\n")
    maxRes.write("Recall:\n")
    #highest = (np.argmax(np.array(res[0])), res[0][np.argmax(np.array(res[0]))])
    mean = np.mean(np.array(res[0]))
    #maxRes.write("index: " + str(highest[0]) + " percent: " + str(highest[1]) + "\n")
    maxRes.write("Percent: " + str(mean) + "\n")

    #highest_pres = (np.argmax(np.array(res[1])), res[1][np.argmax(np.array(res[1]))])
    mean_pres = np.mean(np.array(res[1]))
    maxRes.write("Precision:\n")
    #maxRes.write("index: " + str(highest[0]) + " percent: " + str(highest[1]) + "\n\n")
    maxRes.write("Percent: " + str(mean_pres) + "\n\n")
    plt.savefig(res_dir + "/plots/" + results[game].replace(".txt","") + ".png")
