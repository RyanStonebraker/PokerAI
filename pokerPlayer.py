from hand import Hand

class PokerPlayer:
    def __init__(self, startMoney, ai):
        __money = startMoney
        self.__startHand()

    def __startHand(self):
        self.__hand = Hand()
        self.__hand.addCard()
        self.__hand.addCard()

    def bet(self, currentBet):
        self.__roundDone = False

        betAmount = currentBet

        if betAmount <= currentBet:
            self.__roundDone = True

        return betAmount

    def roundDone(self):
        return self.__roundDone

    __roundDone = False
    __hand = []
    __money = 0
    __betHistory = []
