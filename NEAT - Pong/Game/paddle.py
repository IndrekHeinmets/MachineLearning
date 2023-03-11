import pygame
import os


class Paddle:
    VEL = 6
    WIDTH = 30
    HEIGHT = 100
    IMG = pygame.image.load(os.path.join("assets", "paddle.png"))

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.img = self.IMG

    def draw(self, win):
        rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(self.img, rect.topleft)

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y