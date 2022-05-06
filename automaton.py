class Automaton():
    def __init__(self, config_file):
        self.config_file = config_file
        self.sigma = []
        self.states = []
        self.transitions = []
        print("Hi, I'm an automaton!")

    def validate(self):
        with open(self.config_file, "r") as fin:
            input_str = fin.read()
            if not self.accepts_input(input_str):
                raise Exception("ValidationException")
            else:
                for t in self.transitions:
                    if (t[0] not in self.states) or (t[1] not in self.sigma) or (t[2] not in self.states):
                        raise Exception("ValidationException")
        return True
        
    def accepts_input(self, input_str):
        try:
            self.read_input(input_str)
            return True
        except Exception:
            return False

    def read_input(self, input_str):
        lines = [line for line in input_str.split('\n')]
        n = len(lines) - 1
        i = 0
        while i < n:
            if lines[i][0] != '#':
                part = lines[i].split()[0]
                if part == "Sigma":
                    i += 1
                    while lines[i] != "End":
                        word = lines[i].strip()
                        self.sigma.append(word)
                        i += 1
                    if len(self.sigma) == 0:
                        raise Exception("RejectionException")
                elif part == "States":
                    i += 1
                    init = 0
                    final = 0
                    while lines[i] != "End":
                        state = [w.strip() for w in lines[i].split(',')]
                        self.states.append(state[0])
                        i += 1
                        if 'S' in state:
                            init += 1
                            if init > 1:
                                raise Exception("RejectionException")
                        elif 'F' in state:
                            final += 1
                    if final == 0:
                        raise Exception("RejectionException")
                    if len(self.states) == 0:
                        raise Exception("RejectionException")
                elif part == "Transitions":
                    i += 1
                    while lines[i] != "End":
                        transition = [w.strip() for w in lines[i].split(',')]
                        if len(transition) != 3:
                            raise Exception("RejectionException")
                        self.transitions.append((transition[0], transition[1], transition[2]))
                        i += 1
                    if len(self.transitions) == 0:
                        raise Exception("RejectionException")
                else:
                    raise Exception("RejectionException")    
            i += 1
    

if __name__ == "__main__":
    a = Automaton("automaton.txt")
    print(a.validate())
