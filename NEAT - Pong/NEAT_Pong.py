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

# Window setup:
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEAT - Pong")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.ico")))


class Pong:
    def __init__(self, win, width, height):
        self.game = Game(win, width, height)
        self.left_pad = self.game.left_paddle
        self.right_pad = self.game.right_paddle
        self.ball = self.game.ball

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

pygame.quit()


def run_neat(config_path):
    checkpoint_frequency = 10
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # pop = neat.Checkpointer.restore_checkpoint(os.path.join('checkpoints', 'cp-2'))
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    pop.add_reporter(neat.Checkpointer(checkpoint_frequency, filename_prefix=os.path.join('checkpoints', 'cp-')))



    # if MODE == 'train':
    #     best_genome = pop.run(fitness, MAX_GENERATIONS)
    #     save_gen(best_genome, 'best.genome')
    #     print(f'\nBest genome:\n{best_genome}')
    # elif MODE == 'test':
    #     pop.run(fitness, MAX_GENERATIONS)


if __name__ == "__main__":
    loc_dir = os.path.dirname(__file__)
    config_path = os.path.join(loc_dir, 'config-feedforward.txt')
    run_neat(config_path)

    
