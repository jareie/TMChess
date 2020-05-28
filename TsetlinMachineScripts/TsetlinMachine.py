import numpy as np

#==============================================
#==
#==   Disclaimer: Code was written this way as a start for something
#==   more general. (Useable for other cases.) 
#=    It is not complete for this purpose
#==
#==============================================

class TsetlinMachine():
    def __init__(self, Clauses=0, t=0, S=0, Incremental=True, Convolutional=False, weighted=True, Parallel=True, Bits=7, Window=(8,8)):
        self.clauses = Clauses
        self.threshold = t
        self.s = S
        self.machine = None
        self.convolutional = Convolutional
        self.parallel = Parallel
        self.bits = Bits
        self.incremental = Incremental
        self.windowX = Window[0]
        self.windowY = Window[1]
        self.weigthed = weighted

        #print("Window size:",Window)
        self.format_set = False
        self.class_format = None

        if not self.convolutional:
            self.windowX = 8
            self.windowY = 8

        if not Clauses == 0 or t == 0 or s == 0:
            self.machine = self.GetMachine()
        
        self.setBest = True
        self.tempState = None
        self.tempStateScore = 0


    def Pred(self, inp):
        return self.machine.predict(inp)

    def Votes(self, inp):
        clause_output = self.machine.transform(inp, inverted=False)[0]
        
        amount_classes = int(len(clause_output)/self.clauses)
        scoring = [[0, 0] for i in range(amount_classes)]
        
        weights = self.machine.get_state()
        
        #print(len(clause_output), self.clauses, amount_classes)
        #print(clause_output[:4000])
        for i in range(amount_classes):
            for clause in range(self.clauses):
                vote = clause_output[int((i*self.clauses)+clause)]
                
                if self.weigthed:
                    vote = vote * weights[i][0][clause]
                
                if clause%2 == 0:
                    scoring[i][0] += vote
                else:
                    scoring[i][1] += vote
        #print(score)
        return scoring


    def GetTotalVote(self):
        
        state = self.machine.get_state()

        if not self.weigthed:
            return [[int(self.clauses/2), int(self.clauses/2)] for i in range(len(state))]
        
        weighting = []
        for weights in state:
            #[for, against]
            cur_class = [0,0]
            non = weights[0][::2]
            neg = weights[0][1::2]
            
            for weight in non:
                cur_class[0] += weight
            for weight in neg:
                cur_class[1] += weight
            weighting.append(cur_class)

        return weighting

    def Score(self, inp):
        prediction = self.Pred(inp)
        
        scores = self.Votes(inp)[prediction[0]]
        #print(scores)
        tot_vote = self.GetTotalVote()[prediction[0]]

        non = scores[0]
        neg = scores[1]
        all_voted = non + neg

        tot_vote_non = tot_vote[0]
        tot_vote_neg = tot_vote[1]
        tot_vote = tot_vote_neg + tot_vote_non

        percent_voted = all_voted / tot_vote
        
        percent_for = non / tot_vote_non
        percent_against = neg / tot_vote_neg
        percent_score = percent_for - percent_against

        #percent_score = (non / tot_vote_non) - (neg / tot_vote_neg)
        #percent_voted = (non + neg) / (tot_vote_non + tot_vote_neg)
        return [percent_score, percent_voted]
        
    def MassScore(self, inp):
        print("Prediction time")
        prediction = self.Pred(np.array(inp))
        
        #votes = self.Votes(inp)[prediction[0]]
        #print(scores)
        

        scores = []
        for i in range(len(prediction)):
            cur_score = self.Votes(inp[i])[prediction[i]]
            tot_vote = self.GetTotalVote()[prediction[i]]

            non = cur_score[0]
            neg = cur_score[1]
            all_voted = non + neg

            tot_vote_non = tot_vote[0]
            tot_vote_neg = tot_vote[1]
            tot_vote = tot_vote_neg + tot_vote_non

            percent_voted = all_voted / tot_vote
            
            percent_for = non / tot_vote_non
            percent_against = neg / tot_vote_neg
            percent_score = percent_for - percent_against
            scores.append([prediction[i], [percent_score, percent_voted]])
        #print("return scores")
        return scores

    def PredWVotes(self, inp):
        return [self.Pred(inp), self.Votes(inp)]

    #==============================================
    #==
    #==   Creating the machine
    #==
    #==============================================

    def GetMachine(self):
        if self.convolutional:
            #print("Convolutional type")
            if self.parallel:
                print("parallel")
                from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D as TMCP
                return TMCP(self.clauses, self.threshold, self.s, (self.windowX, self.windowY), weighted_clauses=True, boost_true_positive_feedback=0)
            else:
                from pyTsetlinMachine.tm import MultiClassConvolutionalTsetlinMachine2D as TMC
                return TMC(self.clauses, self.threshold, self.s, (self.windowX, self.windowY), weighted_clauses=True, boost_true_positive_feedback=0)
        else:
            #print("Non-Convolutional type")
            if self.parallel:
                print("parallel")
                from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine as TMP
                return TMP(self.clauses, self.threshold, self.s, weighted_clauses=True, boost_true_positive_feedback=0)
            else:
                from pyTsetlinMachine.tm import MultiClassTsetlinMachine as TM
                return TM(self.clauses, self.threshold, self.s, weighted_clauses=True, boost_true_positive_feedback=0)

    def NewTsetlinMachine(self):
        self.machine = self.GetMachine()


    #==============================================
    #==
    #==   Training Machine and various results
    #==
    #==============================================

    def TrainTsetlin(self, TrainX, TrainY, Epochs, MemSave=False,split=100):
        if not self.format_set:
            self.class_format = (np.unique(TrainY), TrainX[0])
            self.format_set = True
            #print(self.class_format)

        if not MemSave:
            self.machine.fit(TrainX, TrainY, epochs=Epochs, incremental=self.incremental)
            return
        
        partition = int(len(TrainY)/100)
        for i in range(split):
            trainx = TrainX[i*partition:(i+1)*partition]
            trainy = TrainY[i*partition:(i+1)*partition]
            self.machine.fit(trainx, trainy, epochs=Epochs, incremental=self.incremental)



    def TrainWTest(self, Train, Test, Epochs):
        result = []
        print("Training: Clauses=" + str(self.clauses) + ", T=" + str(self.threshold)+ ", S=" + str(self.s))
        
        for i in range(Epochs):
            #print(i)
            #print(Train)
            #print("Training")
            self.TrainTsetlin(Train[0], Train[1], 1)
            #print("Done")
            predictions = self.machine.predict(Test[0])

            intermediateResult = 100*(predictions == Test[1]).mean()

            if intermediateResult > self.tempStateScore:
                self.tempState = self.machine.get_state()
                self.tempStateScore = intermediateResult

            unique = set(predictions)
            amounts = {}
            for j in unique:
                amounts[j] = 0
            #print(amounts)
            for pred in predictions:
                amounts[pred] = amounts[pred] + 1
            print(str(i) + " Accuracy: ", intermediateResult, " predictions: ", amounts)
            result.append(intermediateResult)

        if self.setBest:
            self.machine.set_state(self.tempState)

        return result


    def TrainWTestHighestRes(self, Train, Test, Epochs):
        results = self.TrainWTest(Train, Test, Epochs)
        return np.argmax(np.array(results))

    def TrainWTestLastRes(self, Train, Test, Epochs):
        results = self.TrainWTest(Train, Test, Epochs)
        return results[len(results)-1]


    #==============================================
    #==
    #==   Saving the Machine for easy testing
    #==
    #==============================================

    def SaveMachine(self,filename="Machine",filepath=""):
        import json
        
        states = self.machine.get_state()
        #print("Before")
        #print(states)
        JSONFile = {
            "clauses": self.clauses,
            "threshold": self.threshold,
            "s": self.s,

            "convolutional": self.convolutional,
            "incremental": self.incremental,
            "parallel": self.parallel,

            "bits": self.bits,

            "window_size_x": self.windowX,
            "window_size_y": self.windowY,

            "format": {
                "classes": self.class_format[0].tolist(),
                "example": self.class_format[1].flatten().tolist()
            },

            "state_loc_name": filepath + filename + "_states"
        }
        state = np.array([np.array([i[0], i[1]]) for i in states])
        #print("after")
        #print(np.array(state))
        np.save(filepath + filename + "_states", np.array(state))
        
        save_file = open(filepath + filename + ".json","w")
        y = json.dump(JSONFile,fp=save_file)

        
        #save_file.write(y)

        #print(y)
    
    def LoadData(self, filename="Nothing", filepath="", parallel=True, double_bits=False):
        import json

        load_file = open(filepath + filename + ".json","r")
        JSONdata = json.load(fp=load_file)

        self.clauses = JSONdata["clauses"]
        self.threshold = JSONdata["threshold"]
        self.s = JSONdata["s"]

        self.convolutional = JSONdata["convolutional"]
        self.incremental = JSONdata["incremental"]
        #self.parallel = JSONdata["parallel"]
        self.parallel = parallel

        self.bits = JSONdata["bits"]

        self.windowX = JSONdata["window_size_x"]
        self.windowY = JSONdata["window_size_y"]

        format_classes = np.array(JSONdata["format"]["classes"])
        format_example = None
        
        if self.convolutional:
            if double_bits:
                format_example = np.reshape(np.array(JSONdata["format"]["example"]),(16,8,self.bits))
            else:
                format_example = np.reshape(np.array(JSONdata["format"]["example"]),(8,8,self.bits))
        else:
            format_example = np.array(JSONdata["format"]["example"])
        
        #Allowing pickle opens the loading for malicous loading.
        #Considering loading arrays into seperate files to avoid object loading(pickle)
        states = np.load(JSONdata["state_loc_name"] + ".npy",allow_pickle=True)
        states = [(i[0], i[1]) for i in states]
        
        trainX = np.array([format_example for i in format_classes])

        #Setup new TsetlinMachine to take over for dummy machine
        #when creating class for loading, and set it up
        self.machine = self.GetMachine()
        self.TrainTsetlin(trainX, format_classes, 1)
        self.machine.set_state(np.array(states))

    #==============================================
    #==
    #==   Getting clauses and showing them
    #==
    #==============================================
    def GetClause(self, clas, clause):
        if self.convolutional:
            return self.GetClauseConv(clas, clause)
        else:
            return self.GetClauseNonConv(clas, clause)

    def GetClauseNonConv(self,clas,clause):
        features = int(self.windowX*self.windowY*self.bits)
        clauses = []
        #Times features with 2 since there will be an include feature and a disclude feature
        for i in range(features*2):
            outputbit = self.machine.ta_action(clas,clause,i)
            clauses.append(outputbit)
        #First half of output is non-negated, second half is negated
        output = []

        for i in range((int(features/self.bits)*2)):
            output.append(clauses[i*self.bits : (i+1)*self.bits])

        return output
    
    def GetClauseConv(self, clas, clause):
        window = int(self.windowX*self.windowY*self.bits)
        #Placement = max_window_size - acutal_window_size
        max_window_size = 8
        placement_X = max_window_size - self.windowX
        placement_Y = max_window_size - self.windowY

        window_bits = []
        for i in range(window*2):
            outputbit = self.machine.ta_action(clas,clause,i)
            window_bits.append(outputbit)

        placement_bits = []
        for i in range(window, window + (placement_X + placement_Y)):
            outputbit = self.machine.ta_action(clas,clause,i)
            placement_bits.append(outputbit)

        #returns the clause and its placement on the board(divided into X and Y)
        return [window_bits, (placement_bits[:placement_X], placement_bits[placement_X:])]

    #Optimization could be to not append the different clauses to their own index (arrays in array),
    #but to have all of them in one array
    def GetClauses(self,clas):
        output = []
        for clause in range(self.clauses):
            clause = self.GetClause(clas,clause)
            output.append(clause)
        return output

    def FormClause(self, clause):
        size = int(len(clause)/2)
        negated = clause[:size]
        nonNegated = clause[size:]

        clause = [[0 for j in range(self.bits)] for i in range(size)]

        for i in range(size):
            for bit in range(self.bits):
                negatedBit = negated[i][bit]
                nonNegatedBit = nonNegated[i][bit]
                
                if negatedBit and nonNegatedBit:
                    #Error - -2
                    clause[i][bit] = -2
                elif negatedBit:
                    #Include feature - 1
                    clause[i][bit] = 1
                elif nonNegatedBit:
                    #Exclude feature - -1
                    clause[i][bit] = -1
                #else:
                #    #Dont Care - 0
                #    clause[i] = 0
        return clause
    
    def TurnClause(self,clas):
        clauses = self.GetClauses(clas)
        for i in range(len(clauses)):
            if self.convolutional:
                clause = self.FormClause(clauses[i][0])
                print("-----------------------")
                print("Position:", clause[1][0],clause[1][1])
                if i%2 == 0:
                    #Non-negated
                    print("Non-negated")
                else:
                    #Negated
                    print("Negated")
                print(clause)
            else:
                clause = self.FormClause(clauses[i])
                print("-----------------------")
                if i%2 == 0:
                    #Non-negated
                    print("Non-negated")
                    print(clause)
                else:
                    #Negated
                    print("Negated")
                    print(clause)

#TsetlinMachine = GetMachine(10000, 2.14, 5)
