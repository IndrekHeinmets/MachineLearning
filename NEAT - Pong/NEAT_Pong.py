from Game import Game
import pickle
import pygame
import neat
import time
import os
pygame.font.init()

AR = 18/10
WIN_WIDTH = 1400
WIN_HEIGHT = round(WIN_WIDTH / AR)
FPS = 60

# Window setup:
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEAT - Pong")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.ico")))

game = Game(WIN, WIN_WIDTH, WIN_HEIGHT)

run = True
clock = pygame.time.Clock()
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    # Player 1 controlls:
    if keys[pygame.K_w]:
        game.move_paddle(left=True, up=True)
    if keys[pygame.K_s]:
        game.move_paddle(left=True, up=False)

    # Player 2 controlls:
    if keys[pygame.K_UP]:
        game.move_paddle(left=False, up=True)
    if keys[pygame.K_DOWN]:
        game.move_paddle(left=False, up=False)

    game.loop()
    game.draw(True, True)
    pygame.display.update()

pygame.quit()
