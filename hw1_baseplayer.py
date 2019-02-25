class BasePlayer:
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

    folded = False
    id = -1
    cards = []
    money = 0
