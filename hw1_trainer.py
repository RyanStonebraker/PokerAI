import json
import random
import time

from hw1_game import Game
from hw1_player import Player
from hw1_aiplayer import AIPlayer

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

def playSeries(args):
    totalPlayers = args.humanPlayers + args.aiPlayers
    playerStats = [{"wins": 0, "moneyWon": 0} for _ in range(totalPlayers)]

    totalHandsEval = 0
    startTime = time.time()
    for i in range(0, args.trials):
        players = []
        for aiPlayer in range(args.aiPlayers):
            loadedWeights = loadWeights(args.weightFile[aiPlayer]) if args.weightFile and len(args.weightFile) > aiPlayer else generateRandomWeightSet()
            ai = AIPlayer(args.startMoney, loadedWeights)
            players.append(ai)
        for humanPlayer in range(args.humanPlayers):
            player = Player(args.startMoney)
            players.append(player)

        pokerGame = Game(*players)
        winner = pokerGame.play()
        totalHandsEval += pokerGame.handEvalCount
        playerStats[winner]["wins"] += 1
        playerStats[winner]["moneyWon"] += pokerGame.potValue
    elapsedTime = time.time() - startTime

    return (playerStats, totalHandsEval, elapsedTime, winner, pokerGame)
