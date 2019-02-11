import itertools
import random
from player import Player

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
            callCount = 0
            while callCount < len(self.players):
                for player in self.players:
                    if player.folded:
                        continue
                    move = player.makeMove(self.visibleCards, currentBet, self.potValue, self.betHistory)
                    if move[0] == "fold":
                        callCount += 1
                        continue
                    elif move[0] == "raise":
                        callCount = 0
                        currentBet = move[1]
                        self.potValue += move[1]
                    else:
                        callCount += 1
                        self.potValue += move[1]
                    self.betHistory.append({
                        "id": player.getID(),
                        "move": move[0],
                        "currentBet": currentBet,
                        "potValue": self.potValue
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
        return (self.generateRandomCard(), self.generateRandomCard())

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

    def evaluateHand(self, player):
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

if __name__ == "__main__":
    player1 = Player(1000)
    player2 = Player(1000)
    player3 = Player(1000)
    pokerGame = Game(player1, player2, player3)
    winner = pokerGame.play()
    print("\n\nWinner: Player", winner)
