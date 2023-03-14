from .paddle import Paddle
from .ball import Ball
import pygame
import os
pygame.init()


class GameInformation:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class Game:
    FONT_SIZE = 35
    FONT = pygame.font.SysFont("ariel", FONT_SIZE)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 250, 0)
    BG_IMG = pygame.image.load(os.path.join("assets", "bg.png"))

    def __init__(self, win, win_width, win_height, ball_vel, pad_vel, max_fit):
        self.win_width = win_width
        self.win_height = win_height

        self.ball_vel = ball_vel
        self.pad_vel = pad_vel

        self.left_paddle = Paddle(
            10, self.win_height // 2 - Paddle.HEIGHT // 2, self.pad_vel)
        self.right_paddle = Paddle(
            self.win_width - 10 - Paddle.WIDTH, self.win_height // 2 - Paddle.HEIGHT//2, self.pad_vel)
        self.ball = Ball(self.win_width // 2,
                         self.win_height // 2, self.ball_vel)

        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.win = win
        self.max_fit = max_fit

    def _draw_score(self):
        left_score_text = self.FONT.render(f'{self.left_score}', 1, self.GREEN if self.left_score > self.right_score else (
            self.YELLOW if self.left_score == self.right_score else self.RED))
        right_score_text = self.FONT.render(f'{self.right_score}', 1, self.GREEN if self.right_score > self.left_score else (
            self.YELLOW if self.right_score == self.left_score else self.RED))
        self.win.blit(left_score_text, (self.win_width // 4 -
                      left_score_text.get_width() // 2, 10))
        self.win.blit(right_score_text, (self.win_width *
                      (3 / 4) - right_score_text.get_width() // 2, 10))

    def _draw_hits(self):
        hits_text = self.FONT.render(
            f'{self.left_hits + self.right_hits}', 1, self.WHITE)
        self.win.blit(hits_text, (self.win_width - hits_text.get_width() -
                      15, self.win_height - self.FONT_SIZE + 2))

    def _draw_stats(self):
        stats_text = self.FONT.render(
            f'Fit: {round(self.max_fit, 1)}', 1, self.WHITE)
        self.win.blit(stats_text, (10, self.win_height - self.FONT_SIZE + 2))

    def _draw_divider(self, win_size, aspect_ratio):
        divider_height = win_size[1] // 28
        rect_width = 5 * aspect_ratio
        rect_height = divider_height * aspect_ratio
        for i in range(10, win_size[1], divider_height):
            if i % 2 == 1:
                continue
            rect_y = i * aspect_ratio
            pygame.draw.rect(
                self.win, self.WHITE, (win_size[0] // 2 - rect_width // 2, rect_y, rect_width, rect_height))

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if ball.y + ball.RADIUS >= self.win_height - 10:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                    ball.x_vel *= -1
                    middle_y = left_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / self.ball_vel
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.left_hits += 1

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1
                    middle_y = right_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / self.ball_vel
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.right_hits += 1

    def draw(self, draw_score=True, draw_hits=False, draw_stats=True):
        self.win.fill(self.WHITE)
        self.win.blit(self.BG_IMG, (0, 0))
        self._draw_divider((self.win_width, self.win_height),
                           (self.win_width / self.win_height))

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        if draw_stats:
            self._draw_stats()

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.win)
        self.ball.draw(self.win)

    def move_paddle(self, left=True, up=True):
        if left:
            if up and self.left_paddle.y - self.pad_vel < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.win_height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - self.pad_vel < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.win_height:
                return False
            self.right_paddle.move(up)
        return True

    def loop(self):
        self.ball.move()
        self._handle_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.win_width:
            self.ball.reset()
            self.left_score += 1

        game_info = GameInformation(
            self.left_hits, self.right_hits, self.left_score, self.right_score)
        return game_info

    def reset(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
