import util

class TransportationProblem(object):
    def __init__(self, N, weights):
        self.N = N
        self.weights = weights

    def startState(self):
        return 1

    def isEnd(self, state):
        return state == self.N

    def succAndCost(self, state):
        # return list of (action, newState, cost) tuples
        result = []
        if state + 1 <= self.N:
            result.append(('walk', state + 1, self.weights['walk']))
        if state * 2 <= self.N:
            result.append(('tram', state * 2, self.weights['tram']))
        return result


def printSolution(solution):
    totalCost, history = solution
    print('totalCost: {}'.format(totalCost))
    for item in history:
        print(item)


def backtrackingSearch(problem):
    best = {'cost': float('+inf'), 'history': None}

    def recurse(state, history, totalCost):
        if problem.isEnd(state):
            if totalCost < best['cost']:
                best['cost'] = totalCost
                best['history'] = history
            return
        for action, newState, cost in problem.succAndCost(state):
            recurse(newState, history + [(action, newState, cost)], totalCost + cost)

    recurse(problem.startState(), history=[], totalCost=0)
    return best['cost'], best['history']


def dynamicProgramming(problem):
    cache = {}
    def futureCost(state):
        if problem.isEnd(state):
            return 0
        if state in cache:
            return cache[state][0]
        result = min((cost+futureCost(newState), action, newState, cost) for action, newState, cost in problem.succAndCost(state))
        cache[state] = result
        return result[0]

    state = problem.startState()
    totalCost = futureCost(state)

    history = []
    while not problem.isEnd(state):
        _, action, newState, cost = cache[state]
        history.append((action, newState, cost))
        state = newState

    return futureCost(problem.startState()), history


def uniformCostSearch(problem):
    frontier = util.PriorityQueue()
    frontier.update(problem.startState(), 0)
    while True:
        state, pastCost = frontier.removeMin()
        if problem.isEnd(state):
            return pastCost, []
        for action, newState, cost in problem.succAndCost(state):
            frontier.update(newState, pastCost+cost)


def predict(N, weights):
    # Input (x): N (number of blocks)
    # Output (y): path (sequence of actions)
    problem = TransportationProblem(N, weights)
    totalCost, history = dynamicProgramming(problem)
    return [action for action, newState, cost in history]


def generateExamples():
    trueWeights = {'walk': 1, 'tram': 2}
    return [(N, predict(N, trueWeights)) for N in range(1, 10)]

examples = generateExamples()
print('Training dataset')
for example in examples:
    print(' ', example)

def structuredPerceptron(examples):
    weights = {'walk': 0, 'tram': 0}
    for t in range(100):
        numMistakes = 0
        for N, trueActions in examples:
            preActions = predict(N, weights)
            if preActions != trueActions:
                numMistakes += 1
            for action in trueActions:
                weights[action] -= 1
            for action in preActions:
                weights[action] += 1
        print('Iteration {}, numMistakes = {}, weights = {}'.format(t, numMistakes,weights))
        if numMistakes == 0:
            break


structuredPerceptron(examples)

#problem = TransportationProblem(N=100, weights={'walk': 1,'tram': 2})
#print(problem.succAndCost(9))
#printSolution(backtrackingSearch(problem))
#printSolution(dynamicProgramming(problem))
#printSolution(uniformCostSearch(problem))