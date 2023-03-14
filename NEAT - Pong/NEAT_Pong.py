from Game import Game
import pickle
import pygame
import time
import neat
import os
pygame.font.init()

# Settings: [MODE: 'pp'-(player vs player), 'ap'-(ai(LHS) vs player(RHS)), 'pa'-(player(LHS) vs ai(RHS)), 'aa'-(ai vs ai), 'train'-(ai training configuration), 'restore_train'-(ai training configuration)]
MODE = 'ap'
BEST_GEN_FIT = 26
RESTORE_CHECKPOINT = 29

# Training parameters:
MAX_GENERATIONS = 30
MAX_FIT = 0
CHECKPOINT_FREQUENCY = 1
MAX_HITS = 25
MOVEMENT_WEIGHT = 0.01
ON_SCREEN_WEIGHT = 1
HIT_WEIGHT = 1

# Game parameters:
MAX_BALL_VEL = 10
PAD_VEL = 10
TIME_MULT = 10  # 1 - for Debugging & Observing, 10 - for Optimal Training

# Window parameters:
AR = 18 / 10
WIN_WIDTH = 1400
WIN_HEIGHT = round(WIN_WIDTH / AR)
FPS = 60

# Window setup:
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEAT - Pong")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.ico")))


class Pong:
    def __init__(self, win, width, height, ball_vel, pad_vel, max_fit):
        self.game = Game(win, width, height, MAX_BALL_VEL, PAD_VEL, max_fit)
        self.left_pad = self.game.left_paddle
        self.left_pad.vel = pad_vel
        self.right_pad = self.game.right_paddle
        self.right_pad.vel = pad_vel
        self.ball = self.game.ball
        self.ball.max_vel = ball_vel

    def lhs_player_controlls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.game.move_paddle(left=True, up=True)
        if keys[pygame.K_s]:
            self.game.move_paddle(left=True, up=False)

    def rhs_player_controlls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.game.move_paddle(left=False, up=True)
        if keys[pygame.K_DOWN]:
            self.game.move_paddle(left=False, up=False)

    def run_net_decision(self, net, pad):
        net_out = net.activate(
            (pad.y, self.ball.y, abs(pad.x - self.ball.x)))
        return net_out.index(max(net_out))

    def net_move_pad(self, move, gen, left=True):
        valid = True
        if move == 0:
            gen.fitness -= MOVEMENT_WEIGHT
        elif move == 1:
            valid = self.game.move_paddle(left=left, up=True)
        elif move == 2:
            valid = self.game.move_paddle(left=left, up=False)
        if not valid:
            gen.fitness -= ON_SCREEN_WEIGHT

    def test_ai(self, gen1, gen2, config):
        net1 = neat.nn.FeedForwardNetwork.create(gen1, config)
        net2 = neat.nn.FeedForwardNetwork.create(gen2, config)

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            if MODE == 'pp':
                self.lhs_player_controlls()
                self.rhs_player_controlls()
            elif MODE == 'ap':
                self.net_move_pad(self.run_net_decision(
                    net1, self.left_pad), gen1, left=True)
                self.rhs_player_controlls()
            elif MODE == 'pa':
                self.lhs_player_controlls()
                self.net_move_pad(self.run_net_decision(
                    net2, self.right_pad), gen2, left=False)
            elif MODE == 'aa':
                self.net_move_pad(self.run_net_decision(
                    net1, self.left_pad), gen1, left=True)
                self.net_move_pad(self.run_net_decision(
                    net2, self.right_pad), gen2, left=False)

            _ = self.game.loop()
            self.game.draw(draw_score=True, draw_hits=False, draw_stats=False)
            pygame.display.update()

    def train_ai(self, gen1, gen2, config):
        global MAX_FIT
        st = time.time()
        net1 = neat.nn.FeedForwardNetwork.create(gen1, config)
        net2 = neat.nn.FeedForwardNetwork.create(gen2, config)
        self.gen1, self.gen2 = gen1, gen2

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            self.net_move_pad(self.run_net_decision(
                net1, self.left_pad), gen1, left=True)
            self.net_move_pad(self.run_net_decision(
                net2, self.right_pad), gen2, left=False)

            game_info = self.game.loop()
            self.game.draw(draw_score=False, draw_hits=True, draw_stats=True)
            pygame.display.update()

            # Stop game as soon as one player misses (reduce training time):
            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > MAX_HITS:
                fit = self.calc_fitness(game_info, time.time() - st)
                if fit > MAX_FIT:
                    MAX_FIT = fit
                break
        return False

    def calc_fitness(self, game_info, duration):
        self.gen1.fitness += (game_info.left_hits * HIT_WEIGHT) + duration
        self.gen2.fitness += (game_info.right_hits * HIT_WEIGHT) + duration
        return self.gen1.fitness


def save_gen(gen, genomes_path):
    with open(os.path.join(genomes_path, f'Gen_fit-{round(gen.fitness)}.genome'), 'wb') as f:
        pickle.dump(gen, f)


def load_gen(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


def fitness(genomes, config):
    for c, (_, gen1) in enumerate(genomes):
        gen1.fitness = 0
        for _, gen2 in genomes[min(c + 1, len(genomes) - 1):]:
            gen2.fitness = 0 if gen2.fitness == None else gen2.fitness
            force_quit = Pong(WIN, WIN_WIDTH, WIN_HEIGHT, MAX_BALL_VEL,
                              PAD_VEL, MAX_FIT).train_ai(gen1, gen2, config)
            if force_quit:
                quit()


def run_neat(config_path, genomes_path, cp_rc=False, restore=False, cp_n=None):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    if restore:
        pop = neat.Checkpointer.restore_checkpoint(
            os.path.join(f'checkpoints', f'Cp-{cp_n}'))
    else:
        pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())

    if cp_rc:
        pop.add_reporter(neat.Checkpointer(generation_interval=CHECKPOINT_FREQUENCY,
                         filename_prefix=os.path.join('checkpoints', 'Cp-')))

    if restore:
        best_genome = pop.run(fitness, MAX_GENERATIONS - cp_n)
    else:
        best_genome = pop.run(fitness, MAX_GENERATIONS)

    save_gen(best_genome, genomes_path)
    print(f'\nBest genome:\n{best_genome}')


def run_gen(best_gen_path, config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    Pong(WIN, WIN_WIDTH, WIN_HEIGHT, MAX_BALL_VEL, PAD_VEL, MAX_FIT).test_ai(
        load_gen(best_gen_path), load_gen(best_gen_path), config)


def main(config_path, best_gen_path, genomes_path):
    global MAX_BALL_VEL, PAD_VEL, TIME_MULT
    if MODE == 'pp' or MODE == 'ap' or MODE == 'pa' or MODE == 'aa':
        run_gen(best_gen_path, config_path)
    elif MODE == 'train' or MODE == 'restore_train':
        MAX_BALL_VEL, PAD_VEL = MAX_BALL_VEL * TIME_MULT, PAD_VEL * TIME_MULT
        if MODE == 'train':
            run_neat(config_path, genomes_path,
                     cp_rc=True, restore=False, cp_n=None)
        elif MODE == 'restore_train':
            run_neat(config_path, genomes_path,
                     cp_rc=True, restore=True, cp_n=RESTORE_CHECKPOINT)


if __name__ == "__main__":
    loc_dir = os.path.dirname(__file__)
    config_path = os.path.join(
        loc_dir, 'NEAT_configs', 'config-feedforward.txt')
    best_gen_path = os.path.join(
        loc_dir, 'genomes', f'Gen_fit-{BEST_GEN_FIT}.genome')
    genomes_path = os.path.join(loc_dir, 'genomes')
    main(config_path, best_gen_path, genomes_path)
