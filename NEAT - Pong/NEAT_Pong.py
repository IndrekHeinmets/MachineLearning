from Game import Game
import pickle
import pygame
import neat
import os
pygame.font.init()

AR = 18/10
WIN_WIDTH = 1400
WIN_HEIGHT = round(WIN_WIDTH / AR)
FPS = 60

MAX_GENERATIONS = 50
MODE = 'restore_train' # 'pp'-(player vs player), 'ap'-(ai(LHS) vs player(RHS)), 'pa'-(player(LHS) vs ai(RHS)), 'aa'-(ai vs ai), 'train'-(ai training configuration), 'restore_train'-(ai training configuration)
MAX_BALL_VEL = 8
PAD_VEL = 8

# Window setup:
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEAT - Pong")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.ico")))


class Pong:
    def __init__(self, win, width, height, ball_vel, pad_vel):
        self.game = Game(win, width, height, MAX_BALL_VEL, PAD_VEL)
        self.left_pad = self.game.left_paddle
        self.left_pad.vel = pad_vel
        self.right_pad = self.game.right_paddle
        self.right_pad.vel = pad_vel
        self.ball = self.game.ball
        self.ball.max_vel = ball_vel

    def test_ai(self):
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
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            # Player 2 controlls:
            if keys[pygame.K_UP]:
                self.game.move_paddle(left=False, up=True)
            if keys[pygame.K_DOWN]:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            print(game_info.left_score, game_info.right_score)
            self.game.draw(True, True)
            pygame.display.update()

    def train_ai(self, gen1, gen2, config):
        net1 = neat.nn.FeedForwardNetwork.create(gen1, config)
        net2 = neat.nn.FeedForwardNetwork.create(gen2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            net1_out = net1.activate((self.left_pad.y, self.ball.y, abs(self.left_pad.x - self.ball.x)))
            decision1 = net1_out.index(max(net1_out))

            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            net2_out = net2.activate((self.right_pad.y, self.ball.y, abs(self.right_pad.x - self.ball.x)))
            decision2 = net2_out.index(max(net2_out))

            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()

            self.game.draw(draw_score=True, draw_hits=True)
            pygame.display.update()

            # Stop game as soon as one player misses (reduce training time):
            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > 50:
                self.calc_fitness(gen1, gen2, game_info)
                break

    def calc_fitness(self, gen1, gen2, game_info):
        gen1.fitness += game_info.left_hits
        gen2.fitness += game_info.right_hits


def fitness(genomes, config):
    for c, (_, gen1) in enumerate(genomes):
        if c == len(genomes) - 1:
            break
        gen1.fitness = 0
        for _, gen2 in genomes[c+1:]:
            gen2.fitness = 0 if gen2.fitness == None else gen2.fitness
            pong = Pong(WIN, WIN_WIDTH, WIN_HEIGHT, MAX_BALL_VEL, PAD_VEL)
            pong.train_ai(gen1, gen2, config)



def run_neat(config_path, cp_rc=False, restore=False, cp_n=None):
    checkpoint_frequency = 10
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # pop = neat.Checkpointer.restore_checkpoint(os.path.join('checkpoints', 'cp-12'))
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    pop.add_reporter(neat.Checkpointer(checkpoint_frequency, filename_prefix=os.path.join('checkpoints', 'cp-')))

    best_genome = pop.run(fitness, MAX_GENERATIONS)


def main(config_path):
    global MAX_BALL_VEL, PAD_VEL
    if MODE == 'pp':
        pass
    elif MODE == 'ap' or MODE == 'pa':
        pass
    elif MODE == 'aa':
        pass
    elif MODE == 'train' or MODE == 'restore_train':
            train_speed_mult = 10
            MAX_BALL_VEL, PAD_VEL = MAX_BALL_VEL * train_speed_mult, PAD_VEL * train_speed_mult
            if MODE == 'train':
                run_neat(config_path, cp_rc=False, restore=False, cp_n=None)
            elif MODE == 'restore_train':
                run_neat(config_path, cp_rc=True, restore=True, cp_n=18)


if __name__ == "__main__":
    loc_dir = os.path.dirname(__file__)
    config_path = os.path.join(loc_dir, 'NEAT_configs', 'config-feedforward.txt')
    main(config_path)