from game import Game
from player import Player
from aiplayer import AIPlayer

import json
import random
import time

def generateRandomWeightSet():
    weights = {}
    weights["foldDecisionCardCount"] = random.randint(0, 4)
    weights["foldIfBetPercent"] = random.random()
    weights["foldPercent"] = random.random()
    weights["raiseQuality"] = random.randint(10000, 100000)
    weights["raiseQualityAtCards"] = random.randint(0, 4)
    weights["raisePercent"] = random.random()
    weights["valueQuality"] = random.random()
    return weights

def loadWeights(file):
    with open(file, "r") as fileReader:
        weights = json.load(fileReader)
        return weights

if __name__ == "__main__":
    weights = loadWeights("weights.txt")
    trials = 100
    scores = [0,0,0]

    totalHandsEval = 0
    startTime = time.time()
    for i in range(0, trials):
        randWeights = generateRandomWeightSet()
        randWeights2 = generateRandomWeightSet()
        player1 = AIPlayer(1000, weights)
        player2 = AIPlayer(1000, randWeights)
        player3 = AIPlayer(1000, randWeights2)
        # player3 = Player(1000)
        pokerGame = Game(player1, player2, player3)
        winner = pokerGame.play()
        totalHandsEval += pokerGame.handEvalCount
        scores[winner] += 1
    elapsedTime = time.time() - startTime
    # print("\n\nPlayer {0} won ${1}".format(winner, pokerGame.potValue))
    print("AIPlayer 1:", scores[0], "wins\nAI (Rand) Player 2:", scores[1], "wins\nAI (Rand) Player 3:", scores[2], "wins")
    print("Hands Evaluated:", totalHandsEval/elapsedTime, "moves/second")
    print("Time For {0} games:".format(trials), elapsedTime, "seconds")
