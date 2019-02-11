class Player:
    def __init__(self, money):
        self.folded = False
        self.id = -1
        self.cards = []
        self.money = money

    def getID(self):
        return self.id

    def assignID(self, id):
        self.id = id

    def getCards(self, *cards):
        for card in cards:
            self.cards.append(card)

    def makeMove(self, visibleCards, currentBet, potValue, betHistory):
        move = "call"
        inValue = currentBet if currentBet < self.money else self.money

        print("\nPlayer {0}'s Turn:".format(self.id))
        print("Visible Cards: ", visibleCards)
        print("My Cards: ", self.cards)
        print("My Money: ", self.money)
        print("Current Round Bet: ", currentBet)
        print("Total Pot Value: ", potValue)
        print("Bet History: ", betHistory)
        move = input("Call, Raise, Fold: ").lower()

        if move == "fold":
            self.folded = True
            inValue = 0
        elif move == "raise":
            raiseAmt = input("Raise From ${0} to? ".format(currentBet))
            userEnteredValidNumber = False
            while not userEnteredValidNumber:
                try:
                    raiseAmt = int(raiseAmt)
                    if raiseAmt > currentBet and raiseAmt <= self.money:
                        userEnteredValidNumber = True
                except:
                    userEnteredValidNumber = False
                    raiseAmt = input("Invalid Amount, Try Again: ")
            inValue = raiseAmt

        self.money -= inValue
        return (move, inValue)

    folded = False
    id = -1
    cards = []
    money = 0
