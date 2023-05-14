import copy

automataFileName = input("Enter the automata file name: ").strip()
automataInputFile = open(automataFileName)

nrStates = int(automataInputFile.readline())  # Number of states (0, 1, ..., n-1)
sigma = automataInputFile.readline().split()  # List of input symbols (alphabet)
initialState = int(automataInputFile.readline().strip())  # Initial state
finalStates = [int(x) for x in automataInputFile.readline().split()]  # List of the final states

alphabetDict = {sigma[i]: i for i in range(len(sigma))}  # Dictionary for converting symbols of sigma to numbers

# Initializing Matrix of lists for finding the next state that will act like the delta function
nextStateDelta = [[[] for i in range(len(sigma))] for j in range(nrStates)]

line = automataInputFile.readline()
while line:
    aux = line.split()
    state1 = int(aux[0])
    transition = aux[1]
    state2 = int(aux[2])
    nextStateDelta[state1][alphabetDict[transition]].append(state2)  # Constructing the delta function
    line = automataInputFile.readline()

wordsFileName = input("Enter the words file name: ").strip()
wordsInputFile = open(wordsFileName)

line = wordsInputFile.readline()
while line:
    word = line.strip()  # reading the word
    word = word[1:len(word) - 1]  # removing " "
    initialWord = word  # copy of the word
    currentPath = [[initialState]]
    while word:
        currentSymbol = word[0]
        word = word[1:]
        newCurrentPath = copy.deepcopy(currentPath)  # every iteration we take all the possible paths
        if len(currentPath) == 0:  # if there are no more possible paths we are done
            break
        # counter for how many pops we need to do
        # (based on how many ramifications we have)
        cnt = 0
        index = 0
        while index < len(currentPath):
            currentState = currentPath[index][len(currentPath[index]) - 1]
            nextPossibleStates = nextStateDelta[currentState][alphabetDict[currentSymbol]]
            if len(nextPossibleStates) == 1:
                newCurrentPath[index].extend(nextPossibleStates)
            elif len(nextPossibleStates) > 1:
                cnt += 1
                for nextState in nextPossibleStates:
                    newCurrentPath.append(currentPath[index] + [nextState])
            elif len(nextPossibleStates) == 0:
                newCurrentPath[index] = []
            index += 1
        index = 0
        while index < len(newCurrentPath):
            if len(newCurrentPath[index]) == 0:
                newCurrentPath.pop(index)
                index -= 1
            index += 1
        for index in range(cnt):
            newCurrentPath.pop(0)
        currentPath = copy.deepcopy(newCurrentPath)  # updating the paths
    if initialWord == "":  # case for the word lambda
        initialWord = "λ"
    accepted = False
    if word == "":
        for index in range(len(currentPath)):
            if currentPath[index][len(currentPath[index]) - 1] in finalStates:
                accepted = True
                break
        if accepted:
            print(f"\nString {initialWord} is accepted by automata")
            print("Roads: ")
        for index in range(len(currentPath)):
            if currentPath[index][len(currentPath[index]) - 1] in finalStates:
                print(*currentPath[index], end="\n")
    if not accepted:
        print(f"\nString {initialWord} is not accepted by automata", end="\n")
    line = wordsInputFile.readline()
