import random

class Game:
    def __init__(self, *players):
        self.players = players
        stillBetting = True
        self.potValue = 0

    def play(self):
        id = 0
        for player in self.players:
            player.getCards(self.dealTwoCards())
            player.assignID(id)
            id += 1
        while self.stillBetting:
            currentBet = 10
            for player in self.players:
                if player.folded:
                    continue
                move = player.makeMove(self.visibleCards, self.currentBet, self.potValue, self.betHistory)
                if move[0] == "fold":
                    continue
                elif move[0] == "call":
                    self.potValue += move[1]
                elif move[0] == "raise":
                    currentBet = move[1]
                    self.potValue += move[1]
                self.betHistory.append({
                    "id": player.getID(),
                    "move": move[0],
                    "currentBet": self.currentBet,
                    "potValue": self.potValue,
                    "visibleCards": self.visibleCards
                })
            if len(self.visibleCards) < 5:
                self.addVisibleCard()
            else:
                winner = self.evaluateHands()
                return winner

    def addVisibleCard(self):
        randomCard = self.generateRandomCard()
        self.visibleCards.append(randomCard)

    def dealTwoCards(self):
        return [self.generateRandomCard(), self.generateRandomCard()]

    def generateRandomCard(self):
        chosenIndex = random.randint(0, len(self.possibleCards)-1)
        randomCard = self.possibleCards[chosenIndex]
        del self.possibleCards[chosenIndex]
        return randomCard

    def evaluateHands(self):
        winner = -1
        topScore = 0
        for player in self.players:
            playerScore = self.evaluateHand(player)
            if playerScore > topScore:
                topScore = playerScore
                winner = player.getID()

    def evaluateHand(self):
        # TODO: Evaluate a single poker hand
        return 5

    stillBetting = True
    players = []
    potValue = 0
    betHistory = []
    visibleCards = []
    possibleCards = [
        "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
        "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",
        "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS"
    ]
