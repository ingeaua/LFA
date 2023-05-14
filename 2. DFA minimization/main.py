def buildDFA():

    inputFileName = input("Enter the name of the input file: ").strip()
    inputFile = open(inputFileName)

    states = inputFile.readline().split()  # List of states
    sigma = inputFile.readline().split()  # List of input symbols (alphabet)
    initialState = inputFile.readline().strip()  # Initial state
    finalStates = inputFile.readline().split()  # List of the final states
    delta = {}           # Transitions

    for state in states:
        delta[state] = {letter: None for letter in sigma}

    line = inputFile.readline()
    while line:
        aux = line.split()
        state1 = aux[0]
        transition = aux[1]
        state2 = aux[2]
        delta[state1][transition] = state2
        line = inputFile.readline()

    return states, sigma, initialState, finalStates, delta


def completeDFA(states, sigma, delta):

    # if the dfa is not complete, we add a "sink" state
    isDFAComplete = 1
    for state in states:
        for letter in sigma:
            if delta[state][letter] is None:
                isDFAComplete = 0
                break
        if not isDFAComplete:
            break
    if isDFAComplete:
        return states, delta
    else:
        states.append("sink")
        delta["sink"] = {letter: "sink" for letter in sigma}
        for state in states:
            for letter in sigma:
                if delta[state][letter] is None:
                    delta[state][letter] = "sink"

    return states, delta


def removeUnreachableStates(states, sigma, initialState, finalStates, delta):

    # if there are unreachable states we should remove them
    # we do this by creating a set of states we can get to from the initial state
    # every iteration, for every state that is reachable we add all the states we can get to with every letter from sigma
    # if there are two iterations in a row where the reachable states do not change, we are done
    reachableStates = [initialState]
    newReachableStates = []
    while reachableStates != newReachableStates:
        newReachableStates = reachableStates.copy()
        oneTransitionAway = []
        for state in reachableStates:
            for letter in sigma:
                oneTransitionAway.append(delta[state][letter])
        reachableStates = newReachableStates + oneTransitionAway
        reachableStates = set(reachableStates)
        reachableStates = list(reachableStates)
        reachableStates.sort()

    unreachableStates = states.copy()
    for state in reachableStates:
        unreachableStates.remove(state)

    for state in unreachableStates:
        delta.pop(state)
        states.remove(state)
        if state in finalStates:
            finalStates.remove(state)

    return states, finalStates, delta


def minimization(states, sigma, initialState, finalStates, delta):

    nonFinalStates = [state for state in states if state not in finalStates]
    oldPartition = [nonFinalStates, finalStates]

    # if the automata has at least one final state, we check for partitions
    # if there are no final states we can skip this part because all states will combine into one
    if len(finalStates) > 0:

        while True:

            newPartition = []
            for oldIndex, oldSubset in enumerate(oldPartition):
                newPartition.append([oldPartition[oldIndex][0]])
                for state in oldSubset[1:]:
                    for newIndex, newSubset in enumerate(newPartition):
                        equivalence = True
                        for letter in sigma:
                            if not equivalence:
                                break
                            for oldSubsetIterable in oldPartition:
                                if delta[state][letter] in oldSubsetIterable and delta[newSubset[0]][letter] not in oldSubsetIterable:
                                    equivalence = False
                                    break
                    if equivalence:
                        newPartition[newIndex].append(state)
                    else:
                        newPartition.append([state])

            # doing a deep sort on oldPartition and newPartition so that we can check if they are equal
            for list in oldPartition:
                list.sort()
            for list in newPartition:
                list.sort()
            oldPartition.sort()
            newPartition.sort()

            # if the two partitions are equal, we are done, if not we continue until they are
            if oldPartition == newPartition:
                break
            else:
                oldPartition = newPartition

    # building the new initial state
    newInitialState = ""
    for partition in oldPartition:
        if initialState in partition:
            newInitialState = ''.join(partition)
            break

    # building the new final states list
    newFinalStates = []
    for partition in oldPartition:
        for finalState in finalStates:
            if finalState in partition:
                newFinalStates.append(''.join(partition))
    newFinalStates = set(newFinalStates)
    newFinalStates = sorted(newFinalStates)

    # building the new states list
    newStates = []
    for partition in oldPartition:
        if partition:
            newStates.append(''.join(partition))

    # reconstructing the delta function
    newDelta = {}
    for state in newStates:
        newDelta[state] = {letter: None for letter in sigma}

    for state in states:
        newState = ""
        for index, newStatesList in enumerate(oldPartition):
            if state in newStatesList:
                newState = newStates[index]
                break
        for letter in sigma:
            oldStateTransition = delta[state][letter]
            newStateTransition = ""
            for index, newStatesList in enumerate(oldPartition):
                if oldStateTransition in newStatesList:
                    newStateTransition = newStates[index]
                    break
            newDelta[newState][letter] = newStateTransition

    return newStates, sigma, newInitialState, newFinalStates, newDelta

def removeSinkStates(states, sigma, initialState, finalStates, delta):

    # same stuff as in removeUnreachableStates but here we remove states starting from we can't reach a final state

    nonFinalStates = [state for state in states if state not in finalStates]

    for state in nonFinalStates:
        canReachFinal = False
        reachableStates = [state]
        newReachableStates = []
        while reachableStates != newReachableStates:
            newReachableStates = reachableStates.copy()
            oneTransitionAway = []
            for stateIterable in reachableStates:
                for letter in sigma:
                    oneTransitionAway.append(delta[stateIterable][letter])
            reachableStates = newReachableStates + oneTransitionAway
            reachableStates = set(reachableStates)
            reachableStates = list(reachableStates)
            reachableStates.sort()
        for reachableState in reachableStates:
            if reachableState in finalStates:
                canReachFinal = True
        if not canReachFinal:
            delta.pop(state)
            states.remove(state)
            for stateIterable in states:
                for letter in sigma:
                    if delta[stateIterable][letter] == state:
                        delta[stateIterable][letter] = None

    return states, sigma, initialState, finalStates, delta


def beautifulPrint(states, sigma, initialState, finalStates, delta):

    print()
    print("The minimized automata is: ")
    print()
    print("States:", end=" ")
    if states:
        print(*states, sep=", ")
    else:
        print(initialState)
    print("Sigma:", end=" ")
    print(*sigma, sep=", ")
    print("Initial state: " + initialState)
    print("Final states:", end=" ")
    print(*finalStates, sep=", ")
    print("Delta (transition function):")
    maxLength = max([len(state) for state in states])
    for state in states:
        for letter in sigma:
            if delta[state][letter] is not None:
                printCopy = state
                printCopy = printCopy.rjust(maxLength)
                print(printCopy, end="")
                print("  --- ", end="")
                print(letter, end="")
                print(" --->  ", end="")
                print(delta[state][letter])


states, sigma, initialState, finalStates, delta = buildDFA()

states, delta = completeDFA(states, sigma, delta)

states, finalStates, delta = removeUnreachableStates(states, sigma, initialState, finalStates, delta)

states, sigma, initialState, finalStates, delta = minimization(states, sigma, initialState, finalStates, delta)

states, sigma, initialState, finalStates, delta = removeSinkStates(states, sigma, initialState, finalStates, delta)

beautifulPrint(states, sigma, initialState, finalStates, delta)

