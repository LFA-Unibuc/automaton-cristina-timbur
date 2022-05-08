class Automaton():

    def __init__(self, config_file):
        if config_file is None:
            return
        self.config_file = config_file
        self.sigma = []
        self.states = []
        self.transitions = []
        self.start = ""
        self.finale = []

    def a_sigma(self, line):
        for w in line:
            if w not in ":_" and w.isalnum() == False:
                raise Exception("Exception: Sigma")
        if (len(line.split()) > 1):
            raise Exception("Exception: Sigma")
        return line

    def a_states(self, line):
        for w in line:
            if w not in ["_", " ", ","] and w.isalnum() == False:
                raise Exception("Exception: States")
        state = [w.strip() for w in line.split(",")]
        if ("" in state) or (len(state) > 3):
            raise Exception("Exception: States")        
        if ((len(state) == 1) and (len("".join(state).split()) > 1)) or (state[0] == "_"):
            raise Exception("Exception: States")        
        if (len(state) > 1) and (state[1].strip() not in ["F", "S"]):
                raise Exception("Exception: States")        
        elif (len(state) > 2) and (state[2].strip() not in ["F", "S"]):
                raise Exception("Exception: States")
        if  len(state) == 3 and (state[1] == state[2]) :
            raise Exception("Exception: States")        
        return tuple(state)

    def a_transitions(self, line):
        for w in line:
            if w not in ["_", " ", ",", ":"] and w.isalnum() == False:
                raise Exception("Exception: Transitions")
        state = [w.strip() for w in line.split(",")]
        if (len(state) != 3):
            raise Exception("Exception: Transitions")   
        elif (("_" in state)  or ("" in state)):
            raise Exception("Exception: Transitions")   
        for s in state:
            if (len(s.split()) > 1):
                raise Exception("Exception: Transitions")  
        return tuple(state)
    
    def validate(self):
        with open(self.config_file, "r") as fin:
            input_ = fin.read()
        if (self.accept(input_) == True): 
            for transition in self.transitions:
                if (transition[0] not in [x[0] for x in self.states])  or (transition[1] not in self.sigma) or \
                    (transition[2] not in [x[0] for x in self.states]):
                    raise Exception("ValidationException")
        return True   
    
    def accept(self, input_str):
        cnt = start = 0
        end = 1
        dict_ = {"Sigma": 0, "States": 0, "Transitions": 0}
        stare = ""
        for line in input_str.split("\n"):
            if (line.split() == []) or (len(line) == 0) or (line.strip()[0] == '#'):
                continue
            cnt += 1
            line1 = line
            line = [x.strip() for x in line.split()]
            if (stare == ""):
                if (len(line) != 2) or (line[0] not in ["States", "Transitions", "Sigma", "End"]) or \
                    (line[1] != ":"):
                    raise Exception("AcceptanceException")
                if (line[0] == "End") and ((stare not in dict_) or (dict_[stare] == 0)):
                    raise Exception("AcceptanceException")
                stare = line[0]
                if stare not in ["States", "Transitions", "Sigma"]:
                    raise Exception("AcceptanceException")
                dict_[stare] = 1
                end = 0
            elif (line[0] == "End") and (dict_[stare] == 1):
                end = 1
                stare = ""
            elif (line[0] in ["States", "Transitions"]) and (end == 0):
                raise Exception("AcceptanceException")
            elif (stare == 'Sigma'):
                if (self.a_sigma(line1.strip()) not in self.sigma):
                    self.sigma.append(self.a_sigma(line1.strip()))
                else:
                    raise Exception("AcceptanceException")
            elif (stare == "States"):
                if ((self.a_states(line1.strip()))[0] not in [x[0] for x in self.states]):
                    self.states.append(self.a_states(line1.strip()))
                else:
                    raise Exception("AcceptanceException")
            elif (stare == "Transitions"):
                if (self.a_transitions(line1.strip()) not in self.transitions):
                    self.transitions.append(self.a_transitions(line1.strip()))
                else:
                    raise Exception("AcceptanceException")
        for x in self.states:
            if ('F' in x):
                self.finale.append(x[0])
            if ('S' in x):
                self.start = x[0]
                start += 1
        if (end == 0) or (cnt == 0) or (start != 1):
            raise Exception("AcceptanceException")
        return True
    
if __name__ == "__main__":
    a = Automaton("1.txt")
    print(a.validate())