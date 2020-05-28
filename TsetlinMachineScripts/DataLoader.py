import csv
import numpy as np

#from TsetlinMachine import Translator as Tr
try:
    import Translator as TL
except ImportError:
    from TsetlinMachineScripts import Translator as TL
from sklearn.model_selection import StratifiedKFold


def TransformData(data, bits=12, conv=False, startingplayer=False, startingplayerbits=False):
    transformed = []
    #print("length:",len(data))
    #for i in range(len(data[0])):
    for entry in data:
        #print(i)
        bitboard = entry[0]
        if conv:
            if not startingplayer:
                bitboard = TL.FENtoBits(bitboard,numberOfBits=bits,startingplayerbits=startingplayer)
            else:
                bitboard = TL.FENtoBitsWStartingPlayer(bitboard,numberOfBits=bits)
            bitboard = np.array(bitboard).reshape((8,8,bits))
        else:
            if not startingplayer:
                bitboard = TL.FENtoBits(bitboard,numberOfBits=bits,startingplayerbits=startingplayer)
            else:
                bitboard = TL.FENtoBitsWStartingPlayer(bitboard,numberOfBits=bits)
            bitboard = np.array(bitboard)

        transformed.append([bitboard, entry[1]])
    return transformed

def DataFromCSV(data):
    condition = 2
    if int(data['Result']) < 0:
        condition = 0
    elif int(data['Result']) > 0:
        condition = 1
    
    board = data['Board']
    return [board, condition]

#location = 'Dataset/DataFEN.csv'
def GetData(path='Dataset/DataFEN.csv', includeDraw=True):
    print("Loading data:", path)
    Data = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            transformation = DataFromCSV(row)
            if (not includeDraw) and (transformation[1] == 2):
                continue
            Data.append(transformation)
    
    print("Data loaded")
    return Data

def SpiltDataXY(Data):
    X = []
    Y = []
    #print(Data)
    for i in Data:
        #print(i)
        X.append(i[0])
        Y.append(i[1])
    return (np.array(X), np.array(Y))

def StratifiedIndexes(Data, split=10):
    print("Stratifying data")
    X,Y = SpiltDataXY(Data)

    skf = StratifiedKFold(n_splits=split, random_state=0, shuffle=True)
    #print(SpiltDataXY(Data))
    #print("----------------------")
    #print(Y)
    KFoldData = skf.split(X,Y)

    sets = []
    for train_index,test_index in KFoldData:
        sets.append((train_index,test_index))
    return sets

def DataEntriesClassLogger(Data):
    train = Data[0]
    test = Data[1]

    tU, trainCount = np.unique(train[1],return_counts=True)
    Percent = [int(float(i/float(len(train[1])))*100) for i in trainCount]
    
    print("Amount of training-data: ", len(train[1]), " For each class: ", trainCount, " Percent divide: ", Percent)
    
    tU, testCount = np.unique(test[1],return_counts=True)
    Percent = [int(float(i/float(len(test[1])))*100) for i in testCount]
    
    print("Amount of testing-data: ", len(test[1]), " For each class: ", testCount, " Percent divide: ", Percent)


def StartifiedDataSingleEntry(data=[], index=0, split=10):
    KFoldIndexes = StratifiedIndexes(data, split)

    X,Y = SpiltDataXY(data)
    
    train_index,test_index = KFoldIndexes[index]
    
    X_train, X_test = X[train_index], X[test_index]
    Y_train, Y_test = Y[train_index], Y[test_index]
    return ((X_train, Y_train), (X_test, Y_test))


def StartifiedData(data=[] ,split=10, Logging=True):
    sets = []

    for i in range(split):
        sets.append(StartifiedDataSingleEntry(data, i, split))
    
    if Logging:
        DataEntriesClassLogger(sets[-1])
    
    print("Returning stratified data")
    return sets