import pygame
import math
import random
import os


class Ball:
    RADIUS = 9
    IMG = pygame.image.load(os.path.join("assets", "ball.png"))

    def __init__(self, x, y, ball_vel):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.max_vel = ball_vel
        self.img = self.IMG
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.x_vel = pos * abs(math.cos(angle) * self.max_vel)
        self.y_vel = math.sin(angle) * self.max_vel

    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def draw(self, win):
        rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(self.img, rect.topleft)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(angle) * self.max_vel)
        y_vel = math.sin(angle) * self.max_vel

        self.y_vel = y_vel
        self.x_vel *= -1