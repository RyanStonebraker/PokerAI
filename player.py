class Player:
    def __init__(self):
        self.folded = False
        self.id = -1
        self.cards = []

    def getID(self):
        return self.id

    def assignID(self, id):
        self.id = id

    def getCards(self, *cards):
        for card in cards:
            self.cards.append(card)

    def makeMove(self, visibleCards, currentBet, potValue, betHistory):
        move = "call"
        inValue = currentBet

        print("\nPlayer {0}'s Turn:".format(self.id))
        print("Visible Cards: ", visibleCards)
        print("Current Round Bet: ", currentBet)
        print("Total Pot Value: ", potValue)
        print("Bet History: ", betHistory)
        input()

        return (move, inValue)

    folded = False
    id = -1
    cards = []
