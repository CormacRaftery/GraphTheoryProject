# Regular expression matching
#Cormac Raftery

def shunt(infix):
    #special characters to watch out for with precedence
    specials = {'*': 50, '.': 40, '|': 30, '?':20, '+':10}

    pofix = ""
    stack = ""
    #loop through the string 1 character at a time
    for c in infix:
        #if open bracket push to stack
        if c == '(':
            stack = stack + c
        #if closing bracket pop and push to output until open bracket
        elif c ==')':
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1],stack[:-1]
            stack = stack[:-1]
            #push to stack and sort for precedence
        elif c in specials:
            while stack and specials.get(c,0) <= specials.get(stack[-1],0):
                pofix, stack = pofix + stack[-1],stack[:-1]
            stack = stack + c
        #immediately push alphabet characters
        else:
            pofix=pofix+c
    #push all remaining operators to output
    while stack:
        pofix,stack = pofix + stack[-1],stack[:-1]
    #return postfix regex
    return pofix

#state with 2 arrows
class state:
    label = None
    edge1 = None
    edge2 = None

#NFA represented by initial and accept states
class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    """Compiles postfix regex to NFA"""
    nfastack = []

    for c in pofix:
        #catenation(1 after the other a.b)
        if c == '.':
            #pop 2 NFA
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            #connect first nfa accept state to nfa2 initial state
            nfa1.accept.edge1 = nfa2.initial
            #push NFA to stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)
        #Alternation(1 or the other)
        elif c == '|':
            #pop 2 NFA
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            #create new initial state and let it go either direction
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            #create an accept state for both edges
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            #push new NFA to stack
            newnfa = nfa(initial,accept)
            nfastack.append(newnfa)
        #Zero or more(accept any amount of this)
        elif c == "*":
            #pop 1 NFA
            nfa1 = nfastack.pop()
            #create new initial and accept states
            initial = state()
            accept = state()
            #join the new initial state to nfa1's initial state and the new accept state.
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            #join the old accept state to the new accept state and nfa1's initial state.
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            #push
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        #Zero or One(accept if there is only 0 or 1 of this character)
        elif c == "?":
            #pop 1 NFA
            nfa1 = nfastack.pop()
            #create states
            initial = state()
            accept = state()
            
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
           
            nfa1.accept.edge1 = accept

            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        #One or more(accept if there is atleast 1 of this character)
        elif c == "+":
            #pop 1 NFA
            nfa1 = nfastack.pop()
            #create states
            initial = state()
            accept = state()

            initial.edge1 = nfa1.initial

            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            #push 
            newnfa= nfa(initial,accept)
            nfastack.append(newnfa)
        else:
            #create new states
            accept = state()
            initial = state()
            #join the initial state to the accept state using arrow c
            initial.label = c
            initial.edge1=accept
            #push new nfa to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
    #nfastack should only have a single nfa now
    return nfastack.pop()

def followes(state):
    #create a new set with state as its only member
    states=set()
    states.add(state)

    #check if state has arrows for e
    if state.label is None:
        #check if edge1 is a state.
        if state.edge1 is not None:
            #if theres an edge 1 follow it
            states |= followes(state.edge1)
            #check for edge 2
        if state.edge2 is not None:
            #follow edge 2
            states |= followes(state.edge2)
    #return all states
    return states 


def match(infix,string):

    #shunt and compile the regular expression.
    postfix=shunt(infix)
    nfa=compile(postfix)

    #the current set of states and the next set of states
    current=set()
    next =set()
    #add the initial state to the current set
    current |= followes(nfa.initial)

    #loop for all characters in string and all states.
    for s in string:
        for c in current:
            #check for match
            if c.label==s:
                #if match add the edge1 state to next set.
                next |= followes(c.edge1)
        #set current to next and clear next.
        current = next
        next = set()
    #check if its an accept state
    return (nfa.accept in current)

#hardcoded samples
infixes = ["a.b.c*","a.(b|d).c*","(a.(b|d))*","a.(b.b)*.c"]
strings = ["","abc","abbc","abcc","abad","abbbc"]

running = True
#sentinel controlled while loop
while running:
    option = input("Pick an option: 1. Run data 2. Create new infixes 3. Create new strings ")
    print(option)
    #run
    if option == '1':
        for i in infixes:
            for s in strings:
                print(match(i,s),i,s)
    #delete and add new infixes
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
    #delete and add new strings
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

