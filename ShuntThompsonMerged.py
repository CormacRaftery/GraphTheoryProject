# Regular expression matching
#Cormac Raftery

def shunt(infix):

    specials = {'*': 50, '.': 40, '|': 30, '?':20, '+':10}

    pofix = ""
    stack = ""

    for c in infix:
        if c == '(':
            stack = stack + c
        elif c ==')':
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1],stack[:-1]
            stack = stack[:-1]
        elif c in specials:
            while stack and specials.get(c,0) <= specials.get(stack[-1],0):
                pofix, stack = pofix + stack[-1],stack[:-1]
            stack = stack + c
        else:
            pofix=pofix+c

    while stack:
        pofix,stack = pofix + stack[-1],stack[:-1]

    return pofix

class state:
    label = None
    edge1 = None
    edge2 = None

class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
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
        elif c == "?":
            nfa1 = nfastack.pop()

            initial = state()
            accept = state()

            nfa1.accept.edge1= initial

            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

        elif c == "+":
            nfa1 = nfastack.pop()

            initial = state()
            accept = state()

            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept

            newnfa= nfa(nfa1.initial,accept)
            nfastack.append(newnfa)
        else:
            accept = state()
            initial = state()

            initial.label = c
            initial.edge1=accept

            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

    return nfastack.pop()

def followes(state):
    states=set()
    states.add(state)

    if state.label is None:
        if state.edge1 is not None:
            states |= followes(state.edge1)
        if state.edge2 is not None:
            states |= followes(state.edge2)
    return states 


def match(infix,string):

    postfix=shunt(infix)
    nfa=compile(postfix)

    current=set()
    next =set()

    current |= followes(nfa.initial)

    for s in string:
        for c in current:
            if c.label==s:
                next |= followes(c.edge1)
        current = next
        next = set()

    return (nfa.accept in current)

infixes = ["a.b.c*","a.(b|d).c*","(a.(b|d))*","a.(b.b)*.c"]
strings = ["","abc","abbc","abcc","abad","abbbc"]

running = True

while running:
    option = input("Pick an option: 1. Run data 2. Create new infixes 3. Create new strings ")
    print(option)
    if option == '1':
        for i in infixes:
            for s in strings:
                print(match(i,s),i,s)
    elif option == '2':
        infixes=[]
        creatingInfixes = True
        while creatingInfixes:
            print("Current infixes are: ",infixes)
            infixesOption= input("Press -1 to stop adding infixes ")
            if infixesOption== '-1':
                creatingInfixes=False
            else:
                infixes.append(infixesOption)
    elif option == '3':
        strings=[]
        creatingStrings = True
        while creatingStrings:
            print("Current strings are:",strings)
            stringsOption= input("Press -1 to stop adding strings ")
            if stringsOption== '-1':
                creatingInfixes=False
            else:
                strings.append(stringsOption)
    else:
        print("done")
        running = False
