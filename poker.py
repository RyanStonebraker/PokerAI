# import pygame
# from pygame.locals import *
from pokerPlayer import PokerPlayer
from hand import Hand
import keyboard

# gameRunning = True
#
# pygame.init()
# textFont = pygame.font.SysFont(None, 30)
#
# clock = pygame.time.Clock()
# screen = pygame.display.set_mode((800,600))
# pygame.display.set_caption("Poker AI")
# screen.fill([255,255,255])
# pygame.display.flip()

visibleCards = Hand()

player = PokerPlayer(1000, 1)
opp = PokerPlayer(1000, 0)

totalBet = 0

gameRunning = True
while gameRunning:
    currentBet = 10
    while not player.roundDone() and not opp.roundDone():
        playerBet = player.bet(currentBet)
        if playerBet:
            currentBet = playerBet

        oppBet = opp.bet(currentBet)
        if oppBet:
            currentBet = oppBet

    totalBet += currentBet

    visibleCards.addCard()

    print(visibleCards.showCards())

    try:
        if keyboard.is_pressed('q'):
            break
        else:
            pass
    except:
        pass



# while gameRunning:
#     for event in pygame.event.get():
#         if event.type == KEYDOWN:
#             if event.key == K_q:
#                 gameRunning = False
#             if event.key == K_a:
#                 if visibleCards.cardCount() < 5:
#                     visibleCards.addCard()
#                 print(visibleCards.showCards())
#         elif event.type == QUIT:
#             gameRunning = False
#
#     text = textFont.render('Some Text', True, (100, 100, 100))
#     screen.blit(text, (800 - text.get_width() // 2, 600 - text.get_height() // 2))
#     pygame.display.flip()
#     clock.tick(60)
