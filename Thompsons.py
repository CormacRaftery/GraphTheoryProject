#Thompson's construction
#Cormac Raftery

class state:
    label = None
    edge1 = None
    edge2 = None

class nfa:
    initial = None
    accept = None

    def _init_(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    nfastack = []

    for c in pofix:
        if c == '.':
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            nfa1.accept.edge1 = nfa2.initial

            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)
        elif c == '|':
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept

            newnfa = nfa(initial,accept)
            nfastack.append(newnfa)
        elif c == "*":
            nfa1 = nfastack.pop()

            initial = state()
            accept = state()

            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        else:
            accept = state()
            initial = state()

            initial.label = c
            initial.edge1=accept

            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

    return nfastack.pop()

print(compile("ab.cd.|"))
print(compile("aa.*"))
