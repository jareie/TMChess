from TsetlinMachineScripts import ChessTM
import numpy as np
paral = False
machinepath = "Dataset/data/results/machines/"

def FormClauseConv(clause, winx, winy, bits, playermoving):
    size = int(len(clause[0])/2)
    WindowX = winx
    if playermoving:
        WindowX = winx*2
    clauseBitsInc = clause[0][:size]
    clauseBitsExc = clause[0][size:]
    placement = clause[1]


    #np.reshape(np.array( ), (WindowX, winy, bits))
    clause = []
    for i in range(size):

        if clauseBitsInc[i] and clauseBitsExc[i]:
            clause.append(2)
        elif clauseBitsInc[i]:
            clause.append(1)
        elif clauseBitsExc[i]:
            clause.append(-1)
        else:
            clause.append(0)

    board = np.reshape(np.array(clause), (WindowX, winy, bits))
    #for x in board:
    #    for piece in x:
    #        print(piece)

    return (board, placement)

def GetCla(machi, clas, stuff):
    def sort(inp):
        return inp[1]

    machines = [[] for i in range(len(machi.Machine))]
    for mach in range(len(machines)):
        machine = machi.Machine[mach]
        print(len(machine.machine.get_state()[clas]))
        weights = machine.machine.get_state()[clas][0]
        clauses = machi.Machine[mach].GetClauses(clas)

        claus = []
        for i in range(len(weights)):
            positive = False
            if i%2==0:
                positive = True

            claus.append((FormClauseConv(clauses[i], stuff[0], stuff[1], stuff[2], stuff[3]), weights[i],positive))

        claus.sort(key=sort, reverse=True)
        #print(claus)
        machines[mach] = claus[:15]
    return machines

def WriteFile(filename, clauses):
    clausefile = open(filename, "w")
    for machine in range(len(clauses)):
        clausefile.write("=====================\n")
        clausefile.write("Machine: " + str(machine) + "\n")
        clausefile.write("=====================\n")
        for i in clauses[machine]:

            #print(i)
            clausefile.write("Weights: " + str(i[1]) + " Vote: ")
            if i[2]:
                clausefile.write("For")
            else:
                clausefile.write("Against")
            clausefile.write(" Placement " + str(i[0][1]))
            clausefile.write("\n")
            clausefile.write(str(i[0][0]))
            clausefile.write("\n")
            clausefile.write("----------------------------\n")
    clausefile.close()

def tsmFp3M():
    Tsm1 = ChessTM.RevConvolutional()
    Tsm1.parallel = paral
    Tsm1.Load(machinepath + "3pieces-3x3")
    
    '''states = Tsm1.Machine[0].machine.get_state()
    claues = Tsm1.Machine[0].GetClauses(0)
    print(len(states[0][0]),len(claues))
    for i in range(len(states[0][0])):
        print("---------")
        print(states[0][0][i])
        print(FormClauseConv(claues[i], (3, 3, 12, False)))'''
    #print(clauses[0][1])
    WriteFile("3pieces-3x3-rev-win.txt", GetCla(Tsm1, 1, (3, 3, 12, False)))
    WriteFile("3pieces-3x3-rev-loss.txt", GetCla(Tsm1, 0, (3, 3, 12, False)))
    WriteFile("3pieces-3x3-rev-draw.txt", GetCla(Tsm1, 2, (3, 3, 12, False)))



def tsmFp4M():
    Tsm2 = ChessTM.RevConvolutional()
    Tsm2.parallel = paral
    Tsm2.double_bits = True
    Tsm2.Load(machinepath + "4pieces-5x5-BitsTest")
    
    WriteFile("4pieces-5x5-BitsTest-rev-loss.txt", GetCla(Tsm2, 0, (5, 5, 12, False)))
    WriteFile("4pieces-5x5-BitsTest-rev-win.txt", GetCla(Tsm2, 1, (5, 5, 12, False)))
    #WriteFile("4pieces-5x5-BitsTest-rev-draw.txt", GetCla(Tsm2, 2, (5, 5, 12, False)))

def tsmSp4M():
    Tsm3 = ChessTM.SideSplit()
    Tsm3.parallel = paral
    Tsm3.double_bits = True
    Tsm3.Load(machinepath + "4pieces-5x5-BitsTest")
    
    WriteFile("4pieces-5x5-BitsTest-sidesplit-loss.txt", GetCla(Tsm3, 0, (5, 5, 12, False)))
    WriteFile("4pieces-5x5-BitsTest-sidesplit-win.txt", GetCla(Tsm3, 1, (5, 5, 12, False)))
    #WriteFile("3pieces-3x3-sidesplit-draw.txt", GetCla(Tsm3, 2, (5, 5, 12, False)))

tsmFp3M()
tsmFp4M()
tsmSp4M()
