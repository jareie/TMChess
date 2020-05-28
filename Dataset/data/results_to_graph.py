res_dir = "results"

def FilesInDir(dirPath):
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]
    return files

results = FilesInDir(res_dir)
#results = ["allpieces-7x7_results.txt"]


def DepthFinder(string):
    final_list = []
    previous = []
    
    depth = 0

    for index in range(len(string)):
        string_char = string[index]
        if string_char == "[" or string_char == "(":
            previous = index

            if len(final_list) == 0:
                final_list.append([])
            else:
                depth += 1
                cur = final_list
                for i in range(depth):
                    cur = cur[-1]
                cur.append([])
        
        if string_char == "]" or string_char == ")":
            depth -= 1
            if previous < 0:
                continue
            cur = final_list
            for i in range(depth):
                #print(cur, i)
                cur = cur[-1]
            
            cur[-1][-1] = [float(p) for p in string[previous+1:index].replace(" ","").split(",")]
            previous = -1

    return final_list

import numpy as np
import matplotlib.pyplot as plt

def Graph(dct_list, additionalName):
    addon = additionalName.replace(".txt","")
    
    placement = "plots/"

    def returnFigString(FigName):
        return "\begin{figure}[!h]\n\centering\n\includegraphics[scale=0.50]{" + FigName + ".png}\n\caption{\label{fig:" + FigName + "} "  + FigName +  "}\n\end{figure}"
    
    def returnHighestString(name,value_list):
        return name + " " + str(np.mean(value_list)) + " +- " + str(np.std(value_list)) + "\n"

    overleaf = ""

    highest = ""

    if "Convolutional" in dct_list:
        plt.clf()
        info = dct_list["Convolutional"]
        graph = [[] for i in info[0]]
        higest = []
        for i in range(len(info)):
            
            higest.append(info[i][np.argmax(np.array(info[i]))])
            #print(info[i], higest[-1])
            for j in range(len(info[i])):
                graph[j].append(info[i][j])
        #print(info)
        #print(higest)
        
        avg_list = []
        
        for i in graph:
            temp_list = np.array(i)
            avg_list.append(np.mean(temp_list))
        
        plt.plot(avg_list)
        plt.ylim(0,100)
        #plt.show()
        name = addon + "-Convolutional"
        plt.savefig(placement + name + ".png")
        overleaf += returnFigString(placement + name)
        highest += returnHighestString("Convolutional",higest)

    
    if "Reversed player - black Convolutional" in dct_list:
        plt.clf()
        info = dct_list["Reversed player - black Convolutional"]
        graph = [[] for i in info[0]]
        higest = []
        for i in range(len(info)):
            higest.append(info[i][np.argmax(np.array(info[i]))])
            for j in range(len(info[i])):
                graph[j].append(info[i][j])
        #print(info)
        
        avg_list = []
        for i in graph:
            temp_list = np.array(i)
            avg_list.append(np.mean(temp_list))
        
        plt.plot(avg_list)
        plt.ylim(0,100)
        #plt.show()
        name = addon + "-Reversed player - black Convolutional"
        plt.savefig(placement + name + ".png")
        overleaf += returnFigString(placement + name)
        highest += returnHighestString("Reversed player - black Convolutional",higest)

    if "Seperated starting player Convolutional" in dct_list:
        plt.clf()
        info = dct_list["Seperated starting player Convolutional"]
        #print(info)
        graph1 = [[] for i in info[0][0]]
        graph2 = [[] for i in info[0][0]]
        higest1 = []
        higest2 = []
        #print(len(graph2))
        for i in range(len(info)):
            higest1.append(info[i][0][np.argmax(np.array(info[i][0]))])
            higest2.append(info[i][1][np.argmax(np.array(info[i][1]))])
            for j in range(len(info[i][0])):
                #print(info[i][0][j])
                graph1[j].append(info[i][0][j])
                graph2[j].append(info[i][1][j])
        #print(info)
        
        avg_list_1 = []
        #print(graph1)
        for i in graph1:
            #print(i)
            temp_list = np.array(i)
            avg_list_1.append(np.mean(temp_list))

        avg_list_2 = []
        for i in graph2:
            temp_list = np.array(i)
            avg_list_2.append(np.mean(temp_list))
        
        #print(len(avg_list_1),avg_list_1)
        #plt.subplot(2,1,1)
        plt.plot(avg_list_1)
        plt.ylim(0,100)

        plt.plot(avg_list_2)
        plt.ylim(0,100)

        #plt.show()
        name = addon + "-Seperated starting player Convolutional"
        plt.savefig(placement + name + ".png")
        overleaf += returnFigString(placement + name)
        highest += returnHighestString("Seperated starting player Convolutional - White",higest1)
        highest += returnHighestString("Seperated starting player Convolutional - Black",higest2)

    if "Seperated by result Convolutional" in dct_list:
        plt.clf()
        info = dct_list["Seperated by result Convolutional"]
        #print(info)
        graph1 = [[] for i in info[0][0]]
        graph2 = [[] for i in info[0][0]]
        higest1 = []
        higest2 = []
        #print(len(graph2))
        for i in range(len(info)):
            higest1.append(info[i][0][np.argmax(np.array(info[i][0]))])
            higest2.append(info[i][1][np.argmax(np.array(info[i][1]))])
            for j in range(len(info[i][0])):
                #print(info[i][0][j])
                graph1[j].append(info[i][0][j])
                graph2[j].append(info[i][1][j])
        #print(info)
        
        avg_list_1 = []
        #print(graph1)
        for i in graph1:
            #print(i)
            temp_list = np.array(i)
            avg_list_1.append(np.mean(temp_list))

        avg_list_2 = []
        for i in graph2:
            temp_list = np.array(i)
            avg_list_2.append(np.mean(temp_list))
        
        #print(len(avg_list_1),avg_list_1)
        plt.plot(avg_list_1)
        plt.ylim(0,100)

        plt.plot(avg_list_2)
        plt.ylim(0,100)

        #plt.show()
        name = addon + "-Seperated by result Convolutional"
        plt.savefig(placement + name + ".png")
        overleaf += returnFigString(placement + name)
        highest += returnHighestString("Seperated by result Convolutional - Win",higest1)
        highest += returnHighestString("Seperated by result Convolutional - Other",higest2)

    if "Non Convolutional" in dct_list:
        plt.clf()
        info = dct_list["Non Convolutional" ]
        graph = [[] for i in info[0]]
        higest = []
        for i in range(len(info)):
            higest.append(info[i][np.argmax(np.array(info[i]))])
            for j in range(len(info[i])):
                graph[j].append(info[i][j])
        #print(info)
        
        avg_list = []
        for i in graph:
            temp_list = np.array(i)
            avg_list.append(np.mean(temp_list))
        
        plt.plot(avg_list)
        plt.ylim(0,100)
        #plt.show()
        name = addon + "-Non Convolutional"
        plt.savefig(placement + name + ".png")
        overleaf += returnFigString(placement + name)
        highest += returnHighestString("Non Convolutional",higest)

    open("OverleafFile.txt","a",encoding="utf-8").write(overleaf)
    open(addon + "-BestResults.txt","w",encoding="utf-8").write(highest)

for res_file in results:
    res = open(res_dir + "/" + res_file,"r").readlines()
    res = [i.replace("\n","") for i in res]
    dict_res = {}

    print(res_file)
    for i in range(len(res)):
        if i % 2 == 0:
            #print(res[i])
            dict_res[res[i]] = DepthFinder(res[i+1])[0]

    Graph(dict_res, res_file)
    #print(dict_res["Convolutional"])
    #print(np.array(DepthFinder(res[5])))