import TsetlinMachine as TM
import DataLoader as DL
import Translator as TL

import numpy as np

values = []

def LoadData():
    Data = DL.GetData(transform=False, includeDraw=False)
    TData = []

    bits = 7

    for entry in Data:
        reshaped = TL.FENtoBits(entry[0], bits, True)
        reshaped = np.reshape(reshaped,(8, 8, bits))
        TData.append([reshaped, entry[1]])

    TData = DL.StartifiedData(TData)
    return TData

def CreateNewMachine(data, clause, t, s):
    tm = TM.TsetlinMachine(clause, t, s, True)

    TotRes = []
    for i in data:
        result = tm.TrainWTest(i[0], i[1], 20)
        highest = np.argmax(result)
        TotRes.append(result[highest])
    mean = np.mean(TotRes)
    values.append(([clause, t, s],mean))
    print(mean)
    return mean




def ParamValuesBetween(higher, lower):
    new = []
    for i in range(len(higher)):
        new.append(lower[i] + int((higher[i] - lower[i])/2))
    
    return new

def CheckPair(dat, high, low, depth):
    paramT1 = ParamValuesBetween(high[0], low[0])
    scoreT1 = CreateNewMachine(dat, paramT1[0], paramT1[1], paramT1[2])

    if scoreT1 > high[1]:
        #return CheckPair((paramT1, scoreT1), high)
        return StartFinding(dat, low, (paramT1, scoreT1), high, depth)
    else:
        return high


def StartFinding(dat, low, mid, high, depth):
    depth = depth - 1

    if depth <= 0:
        if low[1] >= mid[1] and low[1] >= high[1]:
            return low
        elif mid[1] >= low[1] and mid[1] >= high[1]:
            return mid
        else:
            return high


    def DoScoring(low, high, depth):
        chosen = []
        paramT = ParamValuesBetween(low[0], high[0])
        scoreT = CreateNewMachine(dat, paramT[0], paramT[1], paramT[2])
        
        if scoreT > high[1]:
            chosen = StartFinding(dat, low, (paramT, scoreT), high, depth)
        else:
            chosen = CheckPair(dat, high, (paramT, scoreT), depth)
        
        return chosen

    
    chosenL = DoScoring(low,mid,depth)
    chosenR = DoScoring(mid, high, depth)

    if chosenL[1] > chosenR[1]:
        return chosenL
    else:
        return chosenR



sCur = [100, 1.0, 1]

prevScore = 0.0
prev = (sCur.copy(), 0.0)
down = False
final = []

dat = LoadData()

for i in range(1,10):
    cur = [int(sCur[0]*(i*2.0)), float(sCur[1]*float(i*2.0)), int(sCur[2]*(i*2.0))]
    score = CreateNewMachine(dat, cur[0], cur[1], cur[2])
    if prevScore < score:
        prevScore = score
    else:
        prev = [int(sCur[0]*((i-1)*2.0)), int(sCur[1]*((i-1)*2.0)), int(sCur[2]*((i-1)*2.0))]
        final = CheckPair(dat, (prev,prevScore), (cur,score), 10)
        break


print(final)