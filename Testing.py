#K-fold for various methods and data sets

from TsetlinMachineScripts import ChessTM as ctm
from TsetlinMachineScripts import DataLoader as DL

clause = 4000
t = 8000
s = 10
epochs = 50

window = (2,2)
bits = 12
player = False

name = "allpieces-2x2-noweighted"

data = DL.GetData(path="Dataset/data/3pieces.csv") + DL.GetData(path="Dataset/data/4pieces.csv") + DL.GetData(path="Dataset/data/5pieces.csv")
#data = DL.GetData(path="Dataset/data/4pieces.csv", includeDraw=True)

#machines = [("Non Convolutional",ctm.NonConvolutional()), ("Convolutional",ctm.Convolutional()), ("Reversed player - black Convolutional",ctm.RevConvolutional()), ("Seperated starting player Convolutional" ,ctm.SideSplit()), ("Seperated by result Convolutional", ctm.ClassesSplit())]
machines = [("Convolutional",ctm.Convolutional())]
#data = DL.StartifiedDataSingleEntry(data=data,index=0)

#print("==================")
#print(data[0][0])
#print("==================")
def Test(inp):
    machine = inp[1]
    machine.bits = bits
    machine.double_bits = player
    machine.window = window
    sdata = machine.DataForm(data)
    allres = machine.KFold(clause, t, s, epochs, sdata, FileName=name, FilePath="Dataset/data/results/machines/")
    print(" - Finished:", inp[0])
    return (inp[0], allres)

#import Workers as w

#results = w.MakeWorkers(Test, machines,10)

resfile = open("Dataset/data/results/" + name + "_results.txt","a")

#results = []
for i in machines:
    res = Test(i)
    resfile.write(str(res[0]))
    resfile.write("\n")
    resfile.write(str(res[1]))
    resfile.write("\n")
    #results.append(res)

resfile.close()
#print(len(data))


#sdata = nc.StratifiedDataSingle(sdata)
#nc.TrainMachine(clause, t, s, epochs, sdata)

#sdata = DL.StartifiedDataSingleEntry(data)
#nc.TrainMachine(clause, t, s, epochs, sdata)
