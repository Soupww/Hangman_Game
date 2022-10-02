from ast import In
from itertools import count
import operator
from os import curdir
from sre_constants import IN

class wordCounts:
    def __init__(self):
        self.totalNumber = 0
        self.wordDict = dict()
        self.sortCount = []

    def readFile(self, fname): #Deal with strings in the file. Get every word and its count.
        with open(fname) as f:
            for line in f:
                cur = line.rstrip().split() 
                count = eval(cur[1])
                self.wordDict[cur[0]] = count
                self.totalNumber += count

    def getItems(self):
        for key, value in self.wordDict.items():
            print(key,value)

    def wordProbability(self, word):
        if word in self.wordDict:
            return self.wordDict[word] / self.totalNumber
        return 0.0

    def sort(self):
        for i in sorted(self.wordDict, key = self.wordDict.get, reverse = True):
            cur = {}
            cur[i] = self.wordDict[i] / self.totalNumber
            self.sortCount.append(cur)
        return self.sortCount

    def mostFrequent(self):
        for i in range(15):
            print(self.sortCount[i])

    def leastFrequent(self):
        for i in range(1, 15):
            print(self.sortCount[-i])
    
    
class Guess:
    def __init__(self, wordCount):
        self.wordCount = wordCount
        self.number = 0
        self.Letterlist = ['-', '-', '-', '-', '-']
        self.correct = list()
        self.incorrect = list()
        self.notUsed = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def __init__(self, wordCount, number, L1, L2, L3, L4, L5, correct, incorrect):
        self.wordCount = wordCount
        self.number = number
        self.Letterlist = [L1, L2, L3, L4, L5]
        self.correct = correct
        self.incorrect = incorrect
        self.notUsed = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.sum = 0.0
        
        for l in self.correct or self.incorrect:
            self.notUsed.remove(l)
 
        for (word, count) in self.wordCount.wordDict.items():
            flag = False
            for i in range(5):
                if self.Letterlist[i] == '_':
                    if word[i] in self.incorrect or word[i] in self.correct:
                        flag = True
                        continue
                else:
                    if not word[i] == self.Letterlist[i]:
                        flag = True
                        continue
            if flag:
                continue
            
            self.sum = self.sum + self.wordCount.wordProbability(word)
        
    def calPosterior(self, word): #Calculate posterior probability.
        if word not in self.wordCount.wordDict:
            return 0.0

        if self.number > 0:
            for i in range(5):
                if self.Letterlist[i] == '_':
                    if word[i] in self.incorrect or  word[i] in self.correct:
                        return 0.0
                else:
                    if not word[i] == self.Letterlist[i]:
                        return 0.0
            return self.wordCount.wordProbability(word) / self.sum
        else:
            return self.wordCount.wordProbability(word)

    def bestGuess(self):
        bestGuess = ('', 0.0)
        for letter in self.notUsed:
            sumProbability = 0.0
            for(word, counts) in self.wordCount.wordDict.items():
                if letter in word:
                    sumProbability += self.calPosterior(word)
                else : 
                    sumProbability += 0.0
            if sumProbability > bestGuess[1]:
                bestGuess = (letter, sumProbability)
        return bestGuess

if __name__ == "__main__":
    wordCount = wordCounts()
    wordCount.readFile("words.txt")

    sortedWc = wordCount.sort()
    wordCount.mostFrequent()
    wordCount.leastFrequent()

    guess1 = Guess(wordCount, 0, '_', '_', '_', '_', '_', [], [])
    print(guess1.bestGuess())

    guess2 = Guess(wordCount, 2, '_', '_', '_', '_', '_', [], ['E', 'A'])
    print(guess2.bestGuess())

    guess3 = Guess(wordCount, 2, 'A', '_', '_', '_', 'S', ['A', 'S'], [])
    print(guess3.bestGuess())

    guess4 = Guess(wordCount, 3, 'A', '_', '_', '_', 'S', ['A', 'S'], ['I'])
    print(guess4.bestGuess())

    guess5 = Guess(wordCount, 5, '_', '_', 'O', '_', '_', ['O'], ['A', 'E', 'M', 'N', 'T'])
    print(guess5.bestGuess())

    guess6 = Guess(wordCount, 2, '_', '_', '_', '_', '_', [], ['E', 'O'])
    print(guess6.bestGuess())

    guess7 = Guess(wordCount, 2, 'D', '_', '_', 'I', '_', ['D', 'I'], [])
    print(guess7.bestGuess())

    guess8 = Guess(wordCount, 3, 'D', '_', '_', 'I', '_', ['D', 'I'], ['A'])
    print(guess8.bestGuess())

    guess9 = Guess(wordCount, 6, '_', 'U', '_', '_', '_', ['U'], ['A', 'E', 'I', 'O', 'S'])
    print(guess9.bestGuess())