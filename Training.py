# The same script as training, just dosent save results, only meant for
# training machines without having to do K-Fold

from TsetlinMachineScripts import ChessTM as ctm
from TsetlinMachineScripts import DataLoader as DL

clause = 4000
t = 8000
s = 10
epochs = 50

window = (5,5)
bits = 12
player = True

name = "5pieces-5x5-bitsTest"

#data = DL.GetData(path="Dataset/data/3pieces.csv") + DL.GetData(path="Dataset/data/4pieces.csv") + DL.GetData(path="Dataset/data/5pieces.csv")
data = DL.GetData(path="Dataset/data/5pieces.csv", includeDraw=True)

#machines = [("Non Convolutional",ctm.NonConvolutional()), ("Convolutional",ctm.Convolutional()), ("Reversed player - black Convolutional",ctm.RevConvolutional()), ("Seperated starting player Convolutional" ,ctm.SideSplit()), ("Seperated by result Convolutional", ctm.ClassesSplit())]
#machines = [("Reversed player - black Convolutional",ctm.RevConvolutional()), ("Seperated starting player Convolutional" ,ctm.SideSplit()), ("Seperated by result Convolutional", ctm.ClassesSplit())]
#machines = [("Seperated starting player Convolutional" ,ctm.SideSplit())]
#machines = [("Seperated by result Convolutional", ctm.ClassesSplit())]
machines = [("Seperated by result Convolutional", ctm.ClassesSplit())]


def Test(inp):
    machine = inp[1]
    machine.bits = bits
    machine.double_bits = player
    machine.window = window
    sdata = machine.DataForm(data)
    dat = machine.StratifiedDataSingle(sdata)
    allres = machine.TrainMachine(clause, t, s, epochs, dat)
    machine.Save(name, "Dataset/data/results/machines/")
    print(" - Finished:", inp[0])
    return (inp[0], allres)

#import Workers as w

#results = w.MakeWorkers(Test, machines,10)

#resfile = open("Dataset/data/results/" + name + "_results.txt","a")

for i in machines:
    res = Test(i)
    #resfile.write(str(res[0]))
    #resfile.write("\n")
    #resfile.write(str(res[1]))
    #resfile.write("\n")
    #results.append(res)

#resfile.close()

