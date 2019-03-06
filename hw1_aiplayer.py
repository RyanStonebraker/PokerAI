from hw1_baseplayer import BasePlayer
from hw1_handevaluator import HandEvaluator

import pprint
import random

class AIPlayer(BasePlayer):
    def __init__(self, money, weights):
        super().__init__(money)
        self.weights = weights

    def printTypeInfo(self):
        pp = pprint.PrettyPrinter(indent=4)
        print("AI Weights:")
        pp.pprint(self.weights)

    def makeMove(self, visibleCards, currentBet, potValue, betHistory):
        move = "call"
        inValue = currentBet if currentBet < self.money else self.money

        currentHand = HandEvaluator(self.cards, visibleCards)
        currentHand.verbose = self.verbose
        currentHandQuality = currentHand.evaluateHand()
        projectedHandMaxQuality, projectedHandAvgQuality = currentHand.findBestPossibleHand(self.weights["sampleSize"])

        varyingChoice = random.random()
        if len(visibleCards) > self.weights["foldDecisionCardCount"] and currentBet > self.weights["foldIfBetPercent"] * self.money and varyingChoice < self.weights["foldPercent"]:
            move = "fold"
            self.folded = True
            inValue = 0
        elif self.money <= currentBet or projectedHandAvgQuality < self.weights["projectedAverageSafety"]:
            move = "call"
            inValue = self.money
        elif projectedHandMaxQuality > self.weights["projectedMaxRisk"] and currentHandQuality > self.weights["raiseQuality"] and len(visibleCards) > self.weights["raiseQualityAtCards"] and varyingChoice < self.weights["raisePercent"]:
            move = "raise"
            raiseChance = random.random()
            inValue = (self.weights["valueQuality"] * currentHandQuality/100000 + (1-self.weights["valueQuality"]) * raiseChance) * self.money


        self.money -= inValue
        return (move, inValue)
