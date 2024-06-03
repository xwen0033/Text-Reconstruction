from typing import Callable, List, Set

import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model


class SegmentationProblem(util.SearchProblem):
    def __init__(self, query: str, unigramCost: Callable[[str], float]):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # ### START CODE HERE ###
        return 0
        # ### END CODE HERE ###

    def isEnd(self, state) -> bool:
        # ### START CODE HERE ###
        return state == len(self.query)
        # ### END CODE HERE ###

    def succAndCost(self, state):
        # ### START CODE HERE ###
        segments = []

        for i in range(state+1, len(self.query)+1):
            segments.append((i-state, i, self.unigramCost(self.query[state:i])))
        return segments
        # ### END CODE HERE ###


def segmentWords(query: str, unigramCost: Callable[[str], float]) -> str:
    if len(query) == 0:
        return ""

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # ### START CODE HERE ###
    state = 0
    words = []
    for i in ucs.actions:
        word = query[state:state+i]
        state = state + i
        words.append(word)
    return ' '.join(words)
    # ### END CODE HERE ###


############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost


class VowelInsertionProblem(util.SearchProblem):
    def __init__(
        self,
        queryWords: List[str],
        bigramCost: Callable[[str, str], float],
        possibleFills: Callable[[str], Set[str]],
    ):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # ### START CODE HERE ###
        return (0, wordsegUtil.SENTENCE_BEGIN)
        # ### END CODE HERE ###

    def isEnd(self, state) -> bool:
        # ### START CODE HERE ###
        index, previousWord = state
        return index == len(self.queryWords)
        # ### END CODE HERE ###

    def succAndCost(self, state):
        # ### START CODE HERE ###
        vowels = []
        index, previousWord = state
        nextWordnovowels = self.queryWords[index]
        nextWords = self.possibleFills(nextWordnovowels)
        if len(nextWords) == 0:
            nextWords = set([nextWordnovowels])
        for nextWord in nextWords:
            cost = self.bigramCost(previousWord, nextWord)
            vowels.append((nextWord, (index + 1, nextWord), cost))
        return vowels
        # ### END CODE HERE ###


def insertVowels(
    queryWords: List[str],
    bigramCost: Callable[[str, str], float],
    possibleFills: Callable[[str], Set[str]],
) -> str:
    # ### START CODE HERE ###
    problem = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)

    words = []
    for word in ucs.actions:
        words.append(word)
    return ' '.join(words)
    # ### END CODE HERE ###


############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem


class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(
        self,
        query: str,
        bigramCost: Callable[[str, str], float],
        possibleFills: Callable[[str], Set[str]],
    ):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # ### START CODE HERE ###
        return (0, wordsegUtil.SENTENCE_BEGIN)
        # ### END CODE HERE ###

    def isEnd(self, state) -> bool:
        # ### START CODE HERE ###
        return state[0] == len(self.query)
        # ### END CODE HERE ###

    def succAndCost(self, state):
        # ### START CODE HERE ###
        index, previousWord = state
        possibleWords = []
        for i in range(index+ 1, len(self.query) + 1):
            nextWordnovowels = self.query[index:i]
            nextWords = self.possibleFills(nextWordnovowels)
            for nextWord in nextWords:
                cost = self.bigramCost(previousWord, nextWord)
                possibleWords.append((nextWord, (i, nextWord), cost))
        return possibleWords
        # ### END CODE HERE ###


def segmentAndInsert(
    query: str,
    bigramCost: Callable[[str, str], float],
    possibleFills: Callable[[str], Set[str]],
) -> str:
    if len(query) == 0:
        return ""
    # ### START CODE HERE ###
    problem = JointSegmentationInsertionProblem(query, bigramCost, possibleFills)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)
    words = []
    for word in ucs.actions:
        words.append(word)
    return ' '.join(words)
    # ### END CODE HERE ###


############################################################

if __name__ == "__main__":
    shell.main()
