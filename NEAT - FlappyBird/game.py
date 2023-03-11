import random
import pygame
import neat
import time
import os
pygame.font.init()

### TO DO ###
# Add ray vizualisation
# Add increasing world_vel over time

WIN_WIDTH = 500
WIN_HEIGHT = 800
WORLD_VEL = 5
FPS = 60

# Window setup:
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEAT - Flappy Bird")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.ico")))

# Load images:
bg_color = 'd' # d = day, n = night
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"bg_{bg_color}.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))

bird_color = 'b' # r = red, y = yellow, b = blue
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"upflap_{bird_color}.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"midflap_{bird_color}.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"downflap_{bird_color}.png")))]

pipe_color = 'g' # g = green, r = red
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"pipe_{pipe_color}.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROT = 25
    ROT_VEL = 20
    MAX_VEL = 16
    VEL_BUFFER = 2
    ANIM_TIME = 5

    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_c = 0
        self.vel = 0
        self.height = self.y
        self.wing_pos = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_c = 0

    def move(self):
        self.tick_c += 1
        dy = (self.vel * self.tick_c) + (1.5 * self.tick_c**2)
        
        if dy >= self.MAX_VEL:
            dy = self.MAX_VEL
        if dy < 0:
            dy -= self.VEL_BUFFER

        self.y = self.y + dy

        if dy < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.wing_pos += 1

        # Cycle through flapping pattern:
        if self.wing_pos < self.ANIM_TIME:
            self.img = self.IMGS[0]
        elif self.wing_pos < self.ANIM_TIME * 2:
            self.img = self.IMGS[1]
        elif self.wing_pos < self.ANIM_TIME * 3:
            self.img = self.IMGS[2]
        elif self.wing_pos < self.ANIM_TIME * 4:
            self.img = self.IMGS[1]
        elif self.wing_pos == (self.ANIM_TIME * 4) + 1:
            self.img = self.IMGS[0]
            self.wing_pos = 0

        # Stop flapping when falling:
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.wing_pos = self.ANIM_TIME * 2

        # Rotate image based on tilt and blit:
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe():
    MIN_HEIGHT, MAX_HEIGHT = 50, 450
    MIN_GAP, MAX_GAP = 120, 220

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 0
        self.top = 0
        self.bottom = 0
        self.TOP_PIPE_IMG = pygame.transform.flip(PIPE_IMG, False, True)
        self.BOTTOM_PIPE_IMG = PIPE_IMG
        self.passed = False
        self.set_height_and_gap()

    def set_height_and_gap(self):
        self.height = random.randrange(self.MIN_HEIGHT, self.MAX_HEIGHT)
        self.gap = random.randrange(self.MIN_GAP, self.MAX_GAP)
        self.top = self.height - self.TOP_PIPE_IMG.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= WORLD_VEL

    def draw(self, win):
        win.blit(self.TOP_PIPE_IMG, (self.x, self.top))
        win.blit(self.BOTTOM_PIPE_IMG, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.TOP_PIPE_IMG)
        bottom_pipe_mask = pygame.mask.from_surface(self.BOTTOM_PIPE_IMG)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_pipe_mask, top_offset)
        b_point = bird_mask.overlap(bottom_pipe_mask, bottom_offset)

        if t_point or b_point:
            return True
        return False


class Base():
    IMG = BASE_IMG
    WIDTH = BASE_IMG.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= WORLD_VEL
        self.x2 -= WORLD_VEL

        # Cycle bases:
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_win(win, bird, pipes, base):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win)
    pygame.display.update()


def main():
    START_X, START_Y = 230, 350
    BASE_HEIGHT = 730
    PIPE_SPAWN_LOC = 650
    score = 0

    bird = Bird(START_X, START_Y)
    base = Base(BASE_HEIGHT)
    pipes = [Pipe(PIPE_SPAWN_LOC)]
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        add_pipe = False
        rem_pipes = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.TOP_PIPE_IMG.get_width() < 0:
                rem_pipes.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
    
        if add_pipe:
            score += 1
            pipes.append(Pipe(PIPE_SPAWN_LOC))

        for rp in rem_pipes:
            pipes.remove(rp)

        if bird.y + bird.img.get_height() >= BASE_HEIGHT:
            pass

        base.move()
        draw_win(WIN, bird, pipes, base)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()