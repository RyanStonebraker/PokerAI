from hw1_baseplayer import BasePlayer
from hw1_handevaluator import HandEvaluator

import random

class AIPlayer(BasePlayer):
    def __init__(self, money, weights):
        super().__init__(money)
        self.weights = weights

    def makeMove(self, visibleCards, currentBet, potValue, betHistory):
        move = "call"
        inValue = currentBet if currentBet < self.money else self.money

        handQuality = HandEvaluator(self.cards, visibleCards).evaluateHand()

        varyingChoice = random.random()
        if len(visibleCards) > self.weights["foldDecisionCardCount"] and currentBet > self.weights["foldIfBetPercent"] * self.money and varyingChoice < self.weights["foldPercent"]:
            move = "fold"
            self.folded = True
            inValue = 0
        elif self.money <= currentBet:
            move = "call"
            inValue = self.money
        elif handQuality > self.weights["raiseQuality"] and len(visibleCards) > self.weights["raiseQualityAtCards"] and varyingChoice < self.weights["raisePercent"]:
            move = "raise"
            raiseChance = random.random()
            inValue = (self.weights["valueQuality"] * handQuality/100000 + (1-self.weights["valueQuality"]) * raiseChance) * self.money


        self.money -= inValue
        return (move, inValue)
