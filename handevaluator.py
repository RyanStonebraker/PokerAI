class HandEvaluator:
    def __init__(self, hand, visibleCards):
        self.cards = []
        self.cardOrder = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        for card in hand:
            self.cards.append(card)
        for card in visibleCards:
            self.cards.append(card)

        self.cards.sort(key=lambda x: x[-1] + x[:-1])

    def evaluateHand(self):
        isRoyalFlush, handValue = self.checkRoyalFlush()
        if not isRoyalFlush:
            isStraightFlush, handValue = self.checkStraightFlush()
        elif not isStraightFlush:
            isFourOfAKind, handValue = self.checkFourKind()
        elif not isFourOfAKind:
            isFullHouse, handValue = self.checkFullHouse()
        elif not isFullHouse:
            isFlush, handValue = self.checkFlush()
        elif not isFlush:
            isStraight, handValue = self.checkStraight()
        elif not isStraight:
            isThreeOfKind, handValue = self.checkThreeKind()
        elif not isThreeOfKind:
            isTwoPair, handValue = self.checkTwoPair()
        elif not isTwoPair:
            isPair, handValue = self.checkPair()
        elif not isPair:
            handValue = self.findHighestCard()
        return handValue

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

    def checkStraightFlush(self):
        highestNumSuites, highestSuite = self.getHighestNumberOfSuites()
        if len(self.cards) < 5 and highestNumSuites >= 5:
            return (False, 0)

        for card in self.cards:
            if card[-1] == highestSuite:
                cardFace = card[:-1]
                cardPlacementIndex = self.cardOrder.index(cardFace)
                sequence = self.cardOrder[cardPlacementIndex:cardPlacementIndex+5]
                isStraightFlush = self.checkSequence(sequence)
                if isStraightFlush:
                    return (isStraightFlush, 90000 + (len(self.cardOrder) - cardPlacementIndex) * 100)

        return (False, 0)


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
        suiteCount = self.getHighestNumberOfSuites()
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
            if card[-1] == highestSuite:
                cardFace = card[:-1]
                cardPlacementIndex = self.cardOrder.index(cardFace)
                sequence = self.cardOrder[cardPlacementIndex:cardPlacementIndex+5]
                isStraight = self.checkFaceSequence(sequence)
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
            highestCardVal = max(highestCardVal, 10000 + (len(self.cardOrder) - self.cardOrder.index(cardFace)) * 10)
        return highestCardVal
