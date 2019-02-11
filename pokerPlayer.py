from hand import Hand

class PokerPlayer:
    def __init__(self, startMoney, ai):
        self.money = startMoney
        self.hand = []
        self.startHand()
        self.fullHand = []
        self.betHistory = []

    def startHand(self):
        self.hand = Hand([])
        self.hand.addCard()
        self.hand.addCard()

    def bet(self, currentBet):
        self.__roundDone = False
        betAmount = currentBet
        move = 0
        print("Current Hand: ", self.hand.showCards())
        moveType = input("Fold, Call, Raise? (0,1,2): ")
        if moveType == "0":
            betAmount = 0
            move = 0
            self.__roundDone = True
        elif moveType == "1":
            betAmount = currentBet
            move = 1
        else:
            move = 2
            raiseAmt = int(input("How much would you like to raise too? (min: ${0}):".format(currentBet)))
            if raiseAmt < currentBet:
                raiseAmt = currentBet
            betAmount = raiseAmt

        return (betAmount, move) # 0 - Folded, 1 - Called, 2 - Raised

    def roundDone(self):
        return self.__roundDone

    def addVisibleCards(self, cards):
        for privCard in self.hand.showCards():
            cards.append(privCard)
        hand = Hand(cards)
        fullHand = hand

    def evaluateHand(self):
        return self.hand.evaluateHand()

    def evaluateFullHand(self):
        return self.fullHand.evaluateHand()

    def showCards(self):
        print(self.hand.showCards())

    __roundDone = False
    hand = []
    fullHand = []
    money = 0
    betHistory = []
