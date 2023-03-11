import pickle
import pygame
import random
import neat
import os
pygame.font.init()

AR = 5 / 8
WIN_HEIGHT = 900
WIN_WIDTH = round(WIN_HEIGHT * AR)
BASE_WORLD_VEL = 5
WORLD_VEL, WORLD_ACC = BASE_WORLD_VEL, 0.1
FLOOR = WIN_HEIGHT - 70
FPS = 45
GEN = 0
HIGH_SCORE = 0
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

MAX_GENERATIONS = 100
MODE = 'train'  # train (train NEAT nn & save best), test (train NEAT nn), run (run existing genome), play (play with manual keboard input)
DRAW_LINES = True
FONT = pygame.font.SysFont("ariel", 40)

# Window setup:
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEAT - FlappyBird")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.ico")))

# Load images:
bg_color = 'd'  # d = day, n = night
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"bg_{bg_color}.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))

bird_color = 'b'  # r = red, y = yellow, b = blue
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"{pos}flap_{bird_color}.png"))) for pos in ['up', 'mid', 'down']]

pipe_color = 'g'  # g = green, r = red
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"pipe_{pipe_color}.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROT = 25
    ROT_VEL = 20
    MAX_VEL = 16
    VEL_BUFFER = 2
    ANIM_TIME = 5

    def __init__(self, x, y, gen, net):
        self.x = x
        self.y = y
        self.gen = gen
        self.net = net
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
    MIN_GAP, MAX_GAP = 200, 250

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


def save_gen(gen, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(gen, f)


def load_gen(filename):
    with open(filename, 'rb') as f:
        gen = pickle.load(f)
    return None, gen


def draw_win(win, birds, pipes, base, score, gen, pipe_i):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = FONT.render(f'Score: {str(score)}', 1, BLACK)
    win.blit(text, (WIN_WIDTH - 5 - text.get_width(), 5))

    text = FONT.render(f'High Score: {str(HIGH_SCORE)}', 1, BLACK if score < HIGH_SCORE or HIGH_SCORE == 0 else GREEN)
    win.blit(text, (WIN_WIDTH - 5 - text.get_width(), 35))

    if MODE == 'train' or MODE == 'test':
        text = FONT.render(f'Gen: {str(gen)}:{MAX_GENERATIONS}', 1, BLACK)
        win.blit(text, (5, 5))

        text = FONT.render(f'Alive: {str(len(birds))}', 1, BLACK if len(birds) > 5 else RED)
        win.blit(text, (5, 35))

    base.draw(win)

    for bird in birds:
        if DRAW_LINES:
            try:
                pygame.draw.line(win, RED, (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                                 (pipes[pipe_i].x + pipes[pipe_i].TOP_PIPE_IMG.get_width() / 2, pipes[pipe_i].height), 4)
                pygame.draw.line(win, RED, (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                                 (pipes[pipe_i].x + pipes[pipe_i].BOTTOM_PIPE_IMG.get_width() / 2, pipes[pipe_i].bottom), 4)
            except IndexError:
                continue
        bird.draw(win)
    pygame.display.update()


def fitness(genomes, config):
    global GEN, WORLD_VEL, WORLD_ACC, HIGH_SCORE
    GEN += 1
    START_X, START_Y = 230, 350
    PIPE_SPAWN_LOC = 650
    birds, score, WORLD_VEL = [], 0, BASE_WORLD_VEL

    for _, gen in genomes:
        gen.fitness = 0
        birds.append(Bird(START_X, START_Y, gen, neat.nn.FeedForwardNetwork.create(gen, config)))

    base = Base(FLOOR)
    pipes = [Pipe(PIPE_SPAWN_LOC)]
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_i = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x + pipes[0].x + pipes[0].TOP_PIPE_IMG.get_width():
                pipe_i = 1
        else:
            run = False
            break

        for bird in birds:
            bird.move()
            bird.gen.fitness += 0.1

            net_out = bird.net.activate((bird.y, abs(bird.y - pipes[pipe_i].height), abs(bird.y - pipes[pipe_i].bottom)))

            if net_out[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem_pipes = []
        for pipe in pipes:
            for c, bird in enumerate(birds):
                if pipe.collide(bird):
                    bird.gen.fitness -= 1
                    birds.pop(c)

                if not pipe.passed and (pipe.x + (pipe.TOP_PIPE_IMG.get_width() / 2)) < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.TOP_PIPE_IMG.get_width() < 0:
                rem_pipes.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            WORLD_VEL += WORLD_ACC
            for bird in birds:
                bird.gen.fitness += 5
            pipes.append(Pipe(PIPE_SPAWN_LOC))

        for rp in rem_pipes:
            pipes.remove(rp)

        for c, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= FLOOR or bird.y < 0:
                birds.pop(c)

        if score > HIGH_SCORE:
            HIGH_SCORE = score

        base.move()
        draw_win(WIN, birds, pipes, base, score, GEN, pipe_i)


def run_gen(config_path, best_gen_path):
    global WORLD_VEL, WORLD_ACC, HIGH_SCORE
    START_X, START_Y = 230, 350
    PIPE_SPAWN_LOC = 650
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    birds, score, WORLD_VEL = [], 0, BASE_WORLD_VEL
    _, gen = load_gen(best_gen_path)
    birds.append(Bird(START_X, START_Y, gen, neat.nn.FeedForwardNetwork.create(gen, config)))
    base = Base(FLOOR)
    pipes = [Pipe(PIPE_SPAWN_LOC)]
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_i = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x + pipes[0].x + pipes[0].TOP_PIPE_IMG.get_width():
                pipe_i = 1
        else:
            run = False
            break

        for bird in birds:
            bird.move()
            bird.gen.fitness += 0.1

            net_out = bird.net.activate((bird.y, abs(bird.y - pipes[pipe_i].height), abs(bird.y - pipes[pipe_i].bottom)))

            if net_out[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem_pipes = []
        for pipe in pipes:
            for c, bird in enumerate(birds):
                if pipe.collide(bird):
                    bird.gen.fitness -= 1
                    birds.pop(c)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.TOP_PIPE_IMG.get_width() < 0:
                rem_pipes.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            WORLD_VEL += WORLD_ACC
            for bird in birds:
                bird.gen.fitness += 5
            pipes.append(Pipe(PIPE_SPAWN_LOC))

        for rp in rem_pipes:
            pipes.remove(rp)

        for c, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= FLOOR or bird.y < 0:
                birds.pop(c)

        if score > HIGH_SCORE:
            HIGH_SCORE = score

        base.move()
        draw_win(WIN, birds, pipes, base, score, GEN, pipe_i)


def manual_play():
    global WORLD_VEL, WORLD_ACC, HIGH_SCORE, DRAW_LINES
    START_X, START_Y = 230, 350
    PIPE_SPAWN_LOC = 650
    DRAW_LINES = False
    score = 0
    birds = [Bird(START_X, START_Y, 0, 0)]
    base = Base(FLOOR)
    pipes = [Pipe(PIPE_SPAWN_LOC)]
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        for bird in birds:
            bird.move()

        add_pipe = False
        rem_pipes, pipe_i = [], 0
        for pipe in pipes:
            for bird in birds:
                if pipe.collide(bird):
                    run = False
                    break
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                if pipe.x + pipe.TOP_PIPE_IMG.get_width() < 0:
                    rem_pipes.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            WORLD_VEL += WORLD_ACC
            pipes.append(Pipe(PIPE_SPAWN_LOC))

        for rp in rem_pipes:
            pipes.remove(rp)

        for bird in birds:
            if bird.y + bird.img.get_height() >= FLOOR or bird.y < 0:
                run = False
                break

        if score > HIGH_SCORE:
            HIGH_SCORE = score

        base.move()
        draw_win(WIN, birds, pipes, base, score, GEN, pipe_i)


def run_neat(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())

    if MODE == 'train':
        best_genome = pop.run(fitness, MAX_GENERATIONS)
        save_gen(best_genome, 'best.genome')
        print(f'\nBest genome:\n{best_genome}')
    elif MODE == 'test':
        pop.run(fitness, MAX_GENERATIONS)


def main(config_path, best_gen_path):
    if MODE == 'train' or MODE == 'test':
        run_neat(config_path)
    elif MODE == 'run':
        run_gen(config_path, best_gen_path)
    elif MODE == 'play':
        manual_play()


if __name__ == '__main__':
    loc_dir = os.path.dirname(__file__)
    config_path = os.path.join(loc_dir, 'NEAT_configs', 'config-feedforward.txt')
    best_gen_path = os.path.join(loc_dir, 'genomes', 'best.genome')
    main(config_path, best_gen_path)
