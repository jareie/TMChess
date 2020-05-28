import random
import numpy as np

'''import TsetlinMachine.TsetlinMachine as TM
import TsetlinMachine.DataLoader as DL
import TsetlinMachine.Translator as TL'''

try:
    import TsetlinMachine as TM
except ImportError:
    print("Trying other import")
    from TsetlinMachineScripts import TsetlinMachine as TM
try:
    import DataLoader as DL
except ImportError:
    print("Trying other import")
    from TsetlinMachineScripts import DataLoader as DL
try:
    import Translator as TL
except ImportError:
    print("Trying other import")
    from TsetlinMachineScripts import Translator as TL

'''
ratio = 0.8

random.seed(2)
random.shuffle(Data)
random.seed(None)

Train = Data[:int(len(Data)*ratio)]
Test = Data[int(len(Data)*ratio):]
'''


class TsetlinMachineVersions:
    def __init__(self, bits, window=(8,8)):
        #Collection of trained instances of the Tsetlin Machine
        self.Machine = []
        self.parallel = True
        self.data = []
        self.bits = bits
        self.window = window
        self.double_bits = False

    #Standard edition of the training.
    def TrainMachine(self):
        pass

    def Load(self):
        pass
    
    def KFold(self):
        pass

    def Save(self):
        pass
    
    def StratifiedData(self, data, split=10):
        return DL.StartifiedData(data, split)

    def StratifiedDataSingle(self, data, index=0, split=10):
        return DL.StartifiedDataSingleEntry(data, index, split)

    def SetData(self,data=[],path=""):
        if path == "":
            self.data = DL.StartifiedDataSingleEntry(data,includeDraw=True)
        else:
            self.data = DL.StartifiedDataSingleEntry(path=path,includeDraw=True)

    def Predict(self, inp):
        if not len(self.Machine) == 1:
            print("Not correct predict. Amount of machines found:",str(len(self.Machine)),"expected 1")
            return 
        
        machine = self.Machine[0]
        bit_board = np.array(TL.FENtoBits(inp, machine.bits, startingplayerbits=self.double_bits))
        
        if machine.convolutional:
            bit_board = np.reshape(bit_board,(1, 8, 8, machine.bits))
        else:
            bit_board = np.reshape(bit_board,(1, 1))
        
        score = machine.Score(bit_board)
        return [machine.Pred(bit_board)[0], score]
    
    def DataForm(self, data):
        pass


class NonConvolutional(TsetlinMachineVersions):
    #Non-convolutional T Machine
    def __init__(self, bits=12):
        super().__init__(bits)
    
    def DataForm(self, data):
        return DL.TransformData(data, self.bits, False, startingplayerbits=self.double_bits)

    def Save(self,FileName,FilePath=""):
        self.Machine[0].SaveMachine(FileName + "-NonConv",FilePath)

    def Load(self,FileName,FilePath=""):
        NewMachineW = TM.TsetlinMachine(Parallel=self.parallel)
        NewMachineW.LoadData(FileName + "-NonConv", FilePath, parallel=self.parallel)
        self.Machine.append(NewMachineW)

    def TrainMachine(self, clause, t, s, epochs, data):
        tm = TM.TsetlinMachine(clause, t, s, Convolutional=False, Bits=self.bits)
        #for train, test in KFoldData:

        res = tm.TrainWTest(data[0], data[1], epochs)
        self.Machine.append(tm)
        return res
    
    def TrainMachineTestPred(self, clause, t, s, epochs, data):
        tm = TM.TsetlinMachine(clause, t, s, Convolutional=False, Bits=self.bits, Window=self.window)
        self.Machine.append(tm)

        scores = []
        for i in range(epochs):
            tm.TrainWTest(data[0], data[1], 1)
            score = 0.0
            total = 0.0
            
            for entry in data[1]:
                if self.Predict(entry[0])[0] == entry[1]:
                    score += 1
                total += 1
            result = (score/total)*100
            score.append(result)
        return results

    def KFold(self, clause, t, s, epochs, dataset, classpred=False, FileName=None,FilePath=""):
        results = []
        split = 10
        for i in range(split):
            print("Split:", i+1)
            data = self.StratifiedDataSingle(dataset,i,split)
            self.Machine = []
            if classpred:
                results.append(self.TrainMachineTestPred(clause, t, s, epochs, data))
            else:
                results.append(self.TrainMachine(clause, t, s, epochs, data))
            
            if not FileName == None:
                self.Save(FileName + "_split_" + str(i),FilePath)
            
        return results

    #def Predict(self, inp):
    #    bit_board = np.array([TL.FENtoBits(inp,self.Machine[0].bits, True)])
    #    return [self.Machine[0].Pred(bit_board), 0]

class Convolutional(TsetlinMachineVersions):
    def __init__(self, bits=12, window=(8,8)):
        super().__init__(bits)
        self.window = window

    def DataForm(self, data):
        return DL.TransformData(data, self.bits, True, startingplayerbits=self.double_bits)
        #return DL.StartifiedDataSingleEntry(tData, index, split)
    
    def Save(self,FileName,FilePath=""):
        self.Machine[0].SaveMachine(FileName + "-conv",FilePath)

    def Load(self,FileName,FilePath=""):
        NewMachineW = TM.TsetlinMachine(Parallel=self.parallel)
        NewMachineW.LoadData(FileName + "-conv", FilePath, parallel=self.parallel, double_bits=self.double_bits)
        self.Machine.append(NewMachineW)


    def TrainMachine(self, clause, t, s, epochs, data):
        tm = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)
        #print(Data[0][0])
        res = tm.TrainWTest(data[0], data[1], epochs)
        #tm.SaveMachine("RevConv1")
        self.Machine.append(tm)
        return res

    def TrainMachineTestPred(self, clause, t, s, epochs, data):
        tm = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)
        self.Machine.append(tm)

        scores = []
        for i in range(epochs):
            tm.TrainWTest(data[0], data[1], 1)
            score = 0.0
            total = 0.0
            
            for entry in data[1]:
                if self.Predict(entry[0])[0] == entry[1]:
                    score += 1
                total += 1
            result = (score/total)*100
            score.append(result)
        return results

    def KFold(self, clause, t, s, epochs, dataset, classpred=False, FileName=None,FilePath=""):
        results = []
        split = 10
        for i in range(split):
            print("Split:", i+1)
            data = self.StratifiedDataSingle(dataset,i,split)
            self.Machine = []
            if classpred:
                results.append(self.TrainMachineTestPred(clause, t, s, epochs, data))
            else:
                results.append(self.TrainMachine(clause, t, s, epochs, data))
            
            if not FileName == None:
                self.Save(FileName + "_split_" + str(i),FilePath)
        return results
    #def Predict(self,inp):
    #    return self.Machine[0].Pred(inp)

class RevConvolutional(Convolutional):
    #Convolutional T Machine - Change black starting to white
    def __init__(self,bits=12):
        super().__init__(bits)
    
    def DataForm(self, data):
        tData = []
        #TestData = [[],[]]
        #train = data[0]
        #test = data[1]
        X = 8
        if self.double_bits:
            X = X*2
        for entry in data:
            reshaped = np.array(TL.FENtoBits(entry[0], self.bits, True, startingplayerbits=self.double_bits))
            #print(len(reshaped))
             
            reshaped = np.reshape(reshaped,(X,8,self.bits))
            
            tData.append([reshaped, entry[1]])
        #print(TrainData)
        return tData
    
    def Save(self,FileName,FilePath=""):
        self.Machine[0].SaveMachine(FileName + "-rev",FilePath)

    def Load(self,FileName,FilePath=""):
        NewMachineW = TM.TsetlinMachine(Parallel=self.parallel)
        NewMachineW.LoadData(FileName + "-rev", FilePath, parallel=self.parallel, double_bits=self.double_bits)
        self.Machine.append(NewMachineW)


    def Predict(self,inp):
        score = 0
        X = 8
        if self.double_bits:
            X = X*2
        
        bit_board = np.array(TL.FENtoBits(inp, self.Machine[0].bits, True,startingplayerbits=self.double_bits))
        inp = np.reshape(bit_board, (1,X,8, self.Machine[0].bits))
        #print(inp)
        #print(self.Machine[0].Pred(inp))
        score = self.Machine[0].Score(inp)
        return [self.Machine[0].Pred(inp)[0], score]

    def MassPredict(self, inp):
        score = 0
        tData = []
        #TestData = [[],[]]
        #train = data[0]
        #test = data[1]
        X = 8
        if self.double_bits:
            X = X*2
        for entry in inp:
            #print(entry)
            reshaped = np.array(TL.FENtoBits(entry, self.bits, True, startingplayerbits=self.double_bits))
            #print(len(reshaped))
             
            reshaped = np.reshape(reshaped,(X,8,self.bits))
            
            tData.append(reshaped)
        #print(TrainData)
        #score = self.Machine[0].Score(inp)
        #return [self.Machine[0].Pred(inp)[0], score]
        return self.Machine[0].MassScore(tData)


class SideSplit(Convolutional):
    #
    #Convolutional T Machine - Seperate Starting player and predict for that
    def __init__(self):
        super().__init__()

    def Save(self,FileName,FilePath=""):
        self.Machine[0].SaveMachine(FileName + "-white",FilePath)
        self.Machine[1].SaveMachine(FileName + "-black",FilePath)

    def Load(self,FileName,FilePath=""):
        NewMachineW = TM.TsetlinMachine(Parallel=self.parallel)
        NewMachineW.LoadData(FileName + "-white", FilePath, parallel=self.parallel)
        self.Machine.append(NewMachineW)

        NewMachineB = TM.TsetlinMachine(Parallel=self.parallel)
        NewMachineB.LoadData(FileName + "-black",FilePath, parallel=self.parallel)
        self.Machine.append(NewMachineB)
        #tmWin.SaveMachine()
    
    def DataForm(self, data):
        black = []
        white = []

        #train = data[0]
        #test = data[1]

        for entry in data:
            #entry = train[0][i]
            Y = entry[1]
            reshaped = TL.FENtoBitsWStartingPlayer(entry[0], self.bits)
            #print("Train",entry)
            player = reshaped[len(reshaped)-1]
            board = reshaped[:len(reshaped)-1]
            newBoard = np.reshape(board, (8,8,self.bits))
            
            if player == 1:
                white.append([newBoard, Y])
            else:
                black.append([newBoard, Y])

        return (white, black)

    def StratifiedDataSingle(self, data, index=0, split=10):
        white = DL.StartifiedDataSingleEntry(data[0], index, split)
        black = DL.StartifiedDataSingleEntry(data[1], index, split)
        return (white, black)

    def TrainMachine(self, clause, t, s, epochs, data):
        white, black = data
        #print(white)
        tmw = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)
        resw = tmw.TrainWTest(white[0], white[1], epochs)
        #print(len(black[0][0]))
        tmb = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)
        resb = tmb.TrainWTest(black[0], black[1], epochs)

        self.Machine.append(tmw)
        self.Machine.append(tmb)
        return (resw, resb)

    def TrainMachineTestPred(self, clause, t, s, epochs, data):
        white, black = data

        tmw = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)
        tmb = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)

        self.Machine.append(tmw)
        self.Machine.append(tmb)

        scores = []
        for i in range(epochs):
            tmw.TrainWTest(white[0], white[1], 1)
            tmb.TrainWTest(black[0], black[1], 1)
            score = 0.0
            total = 0.0
            
            for entry in white[1] + black[1]:
                if self.Predict(entry[0])[0] == entry[1]:
                    score += 1
                total += 1
            result = (score/total)*100
            score.append(result)
        return results

    def Predict(self, inp):
        reshaped = TL.FENtoBitsWStartingPlayer(inp, self.bits)
        player = reshaped[len(reshaped)-1]
        board = reshaped[:len(reshaped)-1]
        newBoard = np.reshape(board, (1,8,8,self.bits))
        #print(len(newBoard))

        if player == 1:
            pred = self.Machine[0].Pred(newBoard)[0]
            score = self.Machine[0].Score(newBoard)
            return [pred,score]
            
        else:
            pred = self.Machine[1].Pred(newBoard)[0]
            score = self.Machine[1].Score(newBoard)
            return [pred,score]
    
    def MassPredict(self, inp):
        black = []
        blackIndex = []
        
        white = []
        whiteIndex = []

        #train = data[0]
        #test = data[1]

        for entry in range(len(inp)):
            #entry = train[0][i]
            reshaped = TL.FENtoBitsWStartingPlayer(data[entry], self.bits)
            #print("Train",entry)
            player = reshaped[len(reshaped)-1]
            board = reshaped[:len(reshaped)-1]
            newBoard = np.reshape(board, (8,8,self.bits))
            
            if player == 1:
                white.append(newBoard)
                whiteIndex.append(entry)
            else:
                black.append(newBoard)
                blackIndex.append(entry)
        
        res = self.Machine[0].MassScore(white) + self.Machine[1].MassScore(black)
        indecies = whiteIndex + blackIndex

        def sorter(inp1):
            return inp1[1]
        
        sorting = []
        for i in range(len(res)):
            sorting.append((res[i],indecies[i]))

        sorting.sort(key=sorter)
        return [i[0] for i in sorting]


        
        

        

class ClassesSplit(Convolutional):
    def __init__(self):
        super().__init__()


    def DataForm(self, data):
        winOther = []
        lossDraw = []
        #draw = []

        convolutional = True

        X = 8
        if self.double_bits:
            X = X*2
        for entry in data:
            reshaped = TL.FENtoBits(entry[0], self.bits,startingplayerbits=self.double_bits)
            if convolutional:
                reshaped = np.reshape(reshaped,(X, 8, self.bits))
            
            if entry[1] == 0:
                lossDraw.append([reshaped, 0])
                winOther.append([reshaped, 0])
            elif entry[1] == 1:
                winOther.append([reshaped, 1])
            else:
                winOther.append([reshaped, 0])
                lossDraw.append([reshaped, 1])
        
        return (winOther, lossDraw)
    
    def StratifiedDataSingle(self, data, index=0, split=10):
        winOther = DL.StartifiedDataSingleEntry(data[0], index, split)
        lossDraw = DL.StartifiedDataSingleEntry(data[1], index, split)
        return (winOther, lossDraw)

    def TrainMachine(self, clause, t, s, epochs, data):
        #draw = []
        winOther,lossDraw = data

        tmWin = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)
        resw = tmWin.TrainWTest(winOther[0], winOther[1], epochs)
        self.Machine.append(tmWin)

        tmLoss = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)
        resl = tmLoss.TrainWTest(lossDraw[0], lossDraw[1], epochs)
        self.Machine.append(tmLoss)
        return (resw,resl)

    def TrainMachineTestPred(self, clause, t, s, epochs, data):
        winOther, lossDraw = data

        tmWin = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)
        tmLoss = TM.TsetlinMachine(clause, t, s, Convolutional=True, Bits=self.bits, Window=self.window)

        self.Machine.append(tmWin)
        self.Machine.append(tmLoss)

        scores = []
        for i in range(epochs):
            tmWin.TrainWTest(winOther[0], winOther[1], 1)
            tmLoss.TrainWTest(lossDraw[0], lossDraw[1], 1)
            score = 0.0
            total = 0.0
            
            for entry in white[1] + black[1]:
                if self.Predict(entry[0])[0] == entry[1]:
                    score += 1
                total += 1
            result = (score/total)*100
            score.append(result)
        return results
    
    def Save(self,FileName,FilePath=""):
        self.Machine[0].SaveMachine(FileName + "-Win",FilePath)
        self.Machine[1].SaveMachine(FileName + "-Other",FilePath)

    def Load(self,FileName,FilePath=""):
        NewMachineWin = TM.TsetlinMachine(Parallel=self.parallel)
        NewMachineWin.LoadData(FileName + "-Win", FilePath, parallel=self.parallel,double_bits=self.double_bits)
        self.Machine.append(NewMachineWin)

        NewMachineOther = TM.TsetlinMachine(Parallel=self.parallel)
        NewMachineOther.LoadData(FileName + "-Other",FilePath, parallel=self.parallel,double_bits=self.double_bits)
        self.Machine.append(NewMachineOther)
        #tmWin.SaveMachine()
    
    def Predict(self, inp):
        X = 8
        if self.double_bits:
            X = X*2
        bit_board = np.array(TL.FENtoBits(inp, self.Machine[0].bits, True, startingplayerbits=self.double_bits))
        inp = np.reshape(bit_board, (1,X,8, self.Machine[0].bits))

        
        pred = self.Machine[0].Pred(inp)[0]
        score = self.Machine[0].Score(inp)
        if pred == 0:
            pred2 = self.Machine[1].Pred(inp)[0]
            score = self.Machine[1].Score(inp)
            if pred2 == 0:
                return [0, score]
            return [2, score]
        else:
            return [1, score]

    def MassPredict(self, inp):
        data = []

        win = []
        winIndex = []
        other = []
        otherIndex = []

        convolutional = True

        X = 8
        if self.double_bits:
            X = X*2
        for entry in inp:
            reshaped = TL.FENtoBits(entry[0], self.bits,startingplayerbits=self.double_bits)
            if convolutional:
                reshaped = np.reshape(reshaped,(X, 8, self.bits))

            data.append(reshaped)
        results = self.Machine[0].MassScore(data)
        for i in range(len(results)):
            if results[i][0] == 1:
                win.append(results[i])
                winIndex.append(i)

            else:
                other.append(results[i])
                otherIndex.append(i)

        otherres = aelf.Machine[1].MassScore(other)

        indecies = winIndex + otherIndex
        res = win + otherres

        def sorter(inp1):
            return inp1[1]
        
        sorting = []
        for i in range(len(res)):
            sorting.append((res[i],indecies[i]))

        sorting.sort(key=sorter)
        return [i[0] for i in sorting]

        