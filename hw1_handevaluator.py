import random

class HandEvaluator:
    def __init__(self, hand, visibleCards=None):
        self.cards = []
        self.verbose = False
        self.cardOrder = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        if visibleCards is not None:
            self.cards.append(hand[0][0])
            self.cards.append(hand[0][1])
            for card in visibleCards:
                self.cards.append(card)
        else:
            self.cards = hand

        self.cards.sort(key=lambda x: str(x[-1] + x[:-1]))

    def evaluateHand(self):
        handValue = -1
        evalOrder = [
            self.checkRoyalFlush,
            self.checkStraightFlush,
            self.checkFourKind,
            self.checkFullHouse,
            self.checkFlush,
            self.checkStraight,
            self.checkThreeKind,
            self.checkTwoPair,
            self.checkPair,
            self.findHighestCard
        ]
        for checkMove in evalOrder:
            isBestMove, handValue = checkMove()
            if isBestMove:
                return handValue

    def cardCompare(self, card):
        cardValue = card[:-1]
        if cardValue == "A":
            return 1
        elif cardValue == "K":
            return 13
        elif cardValue == "Q":
            return 12
        elif cardValue == "J":
            return 11
        else:
            return int(cardValue)

    def getDetailedCards(self, hand=None):
        hand = self.cards if not hand else hand
        clubs = []
        diamonds = []
        hearts = []
        spades = []
        detailedCards = []
        for card in hand:
            suite = card[-1:]
            value = card[:-1]
            detailedCards.append({
                "card": card,
                "suite": suite,
                "value": value
            })
            if suite.lower() == "c":
                clubs.append(card)
            elif suite.lower() == 'd':
                diamonds.append(card)
            elif suite.lower() == 'h':
                hearts.append(card)
            elif suite.lower() == 's':
                spades.append(card)

        suiteCount = {
            "clubs": clubs,
            "diamonds": diamonds,
            "hearts": hearts,
            "spades": spades,
            "maxSuiteCount": max(len(clubs), len(diamonds), len(hearts), len(spades))
        }

        return (detailedCards, suiteCount)


    def checkSequence(self, needed):
        suite = ""
        matched = []
        for card in self.cards:
            cardSuite = card[-1]
            cardFace = card[:-1]
            if cardSuite != suite:
                suite = cardSuite
                matched = []
            if cardFace in needed and cardFace not in matched:
                matched.append(cardFace)
            if len(matched) == len(needed):
                return True
        return False

    def checkFaceSequence(self, needed):
        matched = []
        for card in self.cards:
            cardFace = card[:-1]
            if cardFace in needed and cardFace not in matched:
                matched.append(cardFace)
            if len(matched) == len(needed):
                return True
        return False

    def getHighestNumberOfSuites(self):
        highestNumSuites = 0
        highestSuite = ""

        currentSuite = ""
        currentNum = 0
        for card in self.cards:
            cardSuite = card[-1]
            cardFace = card[:-1]
            if currentSuite != cardSuite:
                currentSuite = cardSuite
                currentNum = 1
            else:
                currentNum += 1
                if currentNum > highestNumSuites:
                    highestSuite = currentSuite
                    highestNumSuites = max(currentNum, highestNumSuites)

        return (highestNumSuites, highestSuite)

    def checkRoyalFlush(self):
        if len(self.cards) < 5 and self.getHighestNumberOfSuites()[0] >= 5:
            return (False, 0)

        needed = ["A", "K", "Q", "J", "10"]
        isRoyalFlush = self.checkSequence(needed)
        if isRoyalFlush:
            return (isRoyalFlush, 100000)
        return (isRoyalFlush, 0)

    def getRoyalFlushProbability(self, hand=None):
        hand = self.cards if not hand else hand
        neededCards = ["A", "K", "Q", "J", "10"]
        openCardsLeft = []
        probability = 0
        dontHave = 0
        for neededCard in neededCards:
            cardInHand = False
            for card in hand:
                if card[:-1] == neededCard:
                    cardInHand = True
                    break
            if not cardInHand:
                openCardsLeft.append(neededCard)
                dontHave += 1

            if len(hand) > 2 and dontHave > 2:
                return probability

        cardsLeftInDeck = len(self.cardOrder) * 4 - len(hand)
        probability = 1
        for card in openCardsLeft:
            probability *= 4/cardsLeftInDeck * (7 - len(hand) - (len(openCardsLeft) - 1))
        return probability


    def checkStraightFlush(self):
        highestNumSuites, highestSuite = self.getHighestNumberOfSuites()
        if len(self.cards) < 5 and highestNumSuites >= 5:
            return (False, 0)

        for card in self.cards:
            if card[-1] == highestSuite:
                cardFace = card[:-1]
                cardPlacementIndex = self.cardOrder.index(cardFace)
                sequence = self.cardOrder[cardPlacementIndex:cardPlacementIndex+5]
                if len(sequence) == 5:
                    isStraightFlush = self.checkSequence(sequence)
                else:
                    isStraightFlush = False
                if isStraightFlush:
                    return (isStraightFlush, 90000 + (len(self.cardOrder) - cardPlacementIndex) * 100)
        return (False, 0)

    # def getStraightFlushProbability(self, hand=None):
    #     hand = self.cards if not hand else hand
    #     longestStreak = []
    #     detailedCards, suiteCount = self.getDetailedCards(hand)
    #
    #     probability = 0
    #
    #     if suiteCount["maxSuiteCount"] + (7 - len(hand)) < 5:
    #         return probability
    #
    #     sortedClubs = suiteCount["clubs"]
    #     sortedClubs.sort(key=self.cardCompare)
    #     clubProbability = 0
    #     longestClubStreak = 0
    #     neededCards = []
    #     lastValue = None
    #     currentStreak = 0
    #     for card in sortedClubs:
    #         cardValue = int(card[:-1].upper().replace("A", "1").replace("K", "13").replace("Q", "12").replace("J", "11"))
    #         if lastValue is None or cardValue == lastValue + 1:
    #             currentStreak += 1
    #             if currentStreak > longestClubStreak:
    #                 longestClubStreak = currentStreak
    #                 neededCards = []
    #                 if longestClubStreak < 5:
    #                     if cardValue > 2:
    #                         neededCards.append(cardValue - 1)
    #                     if cardValue < 14:
    #                         neededCards.append(cardValue + 1)
    #         else:
    #             currentStreak = 0
    #         lastValue == cardValue
    #     print(longestClubStreak, neededCards)


    def checkFourKind(self):
        if len(self.cards) < 4:
            return (False, 0)

        for card in self.cards:
            kind = card[:-1]
            kindCount = 0
            for innerCard in self.cards:
                cardFace = innerCard[:-1]
                if cardFace == kind:
                    kindCount += 1
                    if kindCount >= 4:
                        return (True, 80000 + (len(self.cardOrder) - self.cardOrder.index(cardFace)) * 100)
        return (False, 0)

    def checkFullHouse(self):
        if len(self.cards) < 5:
            return (False, 0)

        threeKindFound = False
        threeKind = ""
        pairFound = False
        pair = ""
        for card in self.cards:
            kind = card[:-1]
            kindCount = 0
            for innerCard in self.cards:
                cardFace = innerCard[:-1]
                if cardFace == kind:
                    kindCount += 1
                    if kindCount >= 3:
                        if not threeKindFound:
                            threeKind = cardFace
                            threeKindFound = True
                            if pairFound:
                                if pair == threeKind:
                                    pair = ""
                                    pairFound = False
                                else:
                                    return (True, 70000 + (len(self.cardOrder) - self.cardOrder.index(threeKind)) * 100 + (len(self.cardOrder) - self.cardOrder.index(pair)))
                    elif kindCount >= 2:
                        pairFound = True
                        pair = cardFace
                        if threeKindFound and threeKind != pair:
                            return (True, 70000 + (len(self.cardOrder) - self.cardOrder.index(threeKind)) * 100 + (len(self.cardOrder) - self.cardOrder.index(pair)))

        return (False, 0)

    def checkFlush(self):
        if len(self.cards) < 5:
            return (False, 0)
        suiteCount = self.getHighestNumberOfSuites()[0]
        if suiteCount >= 5:
            highestCardVal = 0
            for card in self.cards:
                highestCardVal = max(highestCardVal, (len(self.cardOrder) - self.cardOrder.index(card[:-1])) * 10)
            return (True, 60000 + highestCardVal)
        return (False, 0)


    def checkStraight(self):
        if len(self.cards) < 5:
            return (False, 0)

        for card in self.cards:
            cardFace = card[:-1]
            cardPlacementIndex = self.cardOrder.index(cardFace)
            sequence = self.cardOrder[cardPlacementIndex:cardPlacementIndex+5]
            if (len(sequence) == 5):
                isStraight = self.checkFaceSequence(sequence)
            else:
                isStraight = False
            if isStraight:
                highestCardVal = 0
                for card in self.cards:
                    highestCardVal = max(highestCardVal, (len(self.cardOrder) - self.cardOrder.index(cardFace)) * 10)
                return (isStraight, 50000 + highestCardVal)
        return (False, 0)

    def checkThreeKind(self):
        if len(self.cards) < 3:
            return (False, 0)

        for card in self.cards:
            kind = card[:-1]
            kindCount = 0
            for innerCard in self.cards:
                cardFace = innerCard[:-1]
                if cardFace == kind:
                    kindCount += 1
                    if kindCount >= 3:
                        return (True, 40000 + (len(self.cardOrder) - self.cardOrder.index(cardFace)) * 100)

        return (False, 0)


    def checkTwoPair(self):
        if len(self.cards) < 4:
            return (False, 0)

        firstPairFound = False
        firstPair = ""
        secondPairFound = False
        secondPair = ""
        for card in self.cards:
            kind = card[:-1]
            kindCount = 0
            for innerCard in self.cards:
                cardFace = innerCard[:-1]
                if cardFace == kind:
                    kindCount += 1
                    if kindCount >= 2:
                        if firstPairFound:
                            secondPairFound = True
                            secondPair = cardFace
                        else:
                            firstPairFound = True
                            firstPair = cardFace
                        if secondPairFound and firstPair != secondPair:
                            return (True, 30000 + (len(self.cardOrder) - self.cardOrder.index(firstPair)) * 100 + (len(self.cardOrder) - self.cardOrder.index(secondPair)) * 100)
        return (False, 0)

    def checkPair(self):
        for card in self.cards:
            kind = card[:-1]
            kindCount = 0
            for innerCard in self.cards:
                cardFace = innerCard[:-1]
                if cardFace == kind:
                    kindCount += 1
                    if kindCount >= 2:
                        return (True, 20000 + (len(self.cardOrder) - self.cardOrder.index(cardFace)) * 100)
        return (False, 0)

    def findHighestCard(self):
        highestCardVal = 0
        for card in self.cards:
            cardFace = card[:-1]
            highestCardVal = max(highestCardVal, 10000 + (len(self.cardOrder) - self.cardOrder.index(cardFace)) * 10)
        return (True, highestCardVal)

    def getCardsRemaining(self, hand):
        allCards = []
        suite = "CHDS"
        for i in range(4):
            allCards += [face + suite[i] for face in self.cardOrder]
        for card in hand:
            allCards.remove(card)
        return allCards

    def findRandomFilledHandStrength(self, hand):
        hand = self.cards if hand is None else hand

        if len(hand) < 7:
            cardsToChooseFrom = self.getCardsRemaining(hand)
            randIndex = random.randint(0, len(cardsToChooseFrom) - 1)
            hand.append(cardsToChooseFrom[randIndex])
            return self.findRandomFilledHandStrength(hand)

        potentialHand = HandEvaluator(hand)
        handStrength = potentialHand.evaluateHand()
        return handStrength

    def findBestPossibleHand(self, sampleSize, hand=None):
        hand = self.cards if hand is None else hand
        bestHandStrength = 0
        totalHandStrength = 0
        if self.verbose:
            print("Predicting hand strength over", sampleSize, "trials...")
        for i in range(sampleSize):
            randomFilledHandStrength = self.findRandomFilledHandStrength([card for card in hand])
            bestHandStrength = max(bestHandStrength, randomFilledHandStrength)
            totalHandStrength += randomFilledHandStrength
        if self.verbose:
            print("Best Possible Hand:", bestHandStrength, ", Average Possible Hand:", totalHandStrength/sampleSize)
        return (bestHandStrength, totalHandStrength/sampleSize)

# if __name__ == "__main__":
#     hand = [('5C', '2C')]
#     visibleCards = ['AC', 'KD']
#     eval = HandEvaluator(hand, visibleCards)
#     print(eval.findBestPossibleHand(10))
    # print(eval.getRoyalFlushProbability())
    # eval.getStraightFlushProbability()
    # print(eval.evaluateHand())
