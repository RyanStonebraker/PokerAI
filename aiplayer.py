from baseplayer import BasePlayer

class AIPlayer(BasePlayer):
    __init__(self, money):
        super().__init__(money)

    def makeMove(self, visibleCards, currentBet, potValue, betHistory):
        move = "call"
        inValue = currentBet if currentBet < self.money else self.money

        

        self.money -= inValue
        return (move, inValue)
