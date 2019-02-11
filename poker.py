from pokerPlayer import PokerPlayer
from hand import Hand
import keyboard

player = PokerPlayer(1000, 1)
opp = PokerPlayer(1000, 0)
visibleCards = Hand([])

totalBet = 0

gameRunning = True
folded = ""
while gameRunning:
    print("Visible Cards:", visibleCards.showCards())

    currentBet = 0
    roundDone = False if folded == "" else True
    calledCount = 0
    while not roundDone:
        print("Player ", end="")
        playerBet = player.bet(currentBet)
        if playerBet[1] == 0:
            roundDone = True
            folded = "Player"
        elif playerBet[1] == 1:
            calledCount += 1
        elif playerBet[1] == 2:
            currentBet = playerBet[0]
            calledCount = 0

        if calledCount >= 2 or roundDone:
            break

        print("Opp ", end="")
        oppBet = opp.bet(currentBet)
        if oppBet[1] == 0:
            roundDone = True
            folded = "Opp"
        elif oppBet[1] == 1:
            calledCount += 1
        elif oppBet[1] == 2:
            currentBet = oppBet[0]
            calledCount = 0

        if calledCount >= 2:
            break

    totalBet += currentBet
    if visibleCards.cardCount() >= 5:
        if folded != "":
            winner = "Player" if "Player" != folded else "Opp"
        else:
            playerScore = player.evaluateFullHand()
            oppScore = opp.evaluateFullHand()

            winner = "Player" if playerScore > oppScore else "Opp"

        print("WINNER:", winner)
        break
    elif visibleCards.cardCount() < 5:
        visibleCards.addCard()
        player.addVisibleCards(visibleCards.showCards())
        opp.addVisibleCards(visibleCards.showCards())


    try:
        if keyboard.is_pressed('q'):
            break
        else:
            pass
    except:
        pass
