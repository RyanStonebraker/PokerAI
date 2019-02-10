import pygame
from pygame.locals import *

gameRunning = True

pygame.init()

screen = pygame.display.set_mode((800,600))

while gameRunning:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                gameRunning = False
        elif event.type == QUIT:
            gameRunning = False
