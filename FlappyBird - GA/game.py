import pygame
import random
import sys

pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.display.set_caption('FlappyBird')
WIDTH = 576
HEIGHT = 1024
FPS = 60
GRAVITY = 0.25
SCROLL_SPEED = 4
FONT_SIZE = 40
CENTRAL_OFFSET = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_font = pygame.font.Font('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\04B_19.TTF', FONT_SIZE)

# Game over message
game_over_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\gameover.png').convert_alpha(), (346, 76))
game_over_rect = game_over_surf.get_rect(center = ((WIDTH / 2, 300)))

# Sounds
flap_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\wing.wav')
hit_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\hit.wav')
death_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\die.wav')
point_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\point.wav')
swoosh_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\swoosh.wav')

# Background
bg_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\background-day.png').convert(), (WIDTH, HEIGHT))
floor_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\base.png').convert(), (WIDTH, int(HEIGHT / 4)))
floor_x = 0

# Bird
bird_down_flap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-downflap.png').convert_alpha(), (44, 31))
bird_mid_flap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-midflap.png').convert_alpha(), (44, 31))
bird_up_flap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-upflap.png').convert_alpha(), (44, 31))
bird_frames = [bird_down_flap, bird_mid_flap, bird_up_flap]
bird_index = 0
bird_surf = bird_frames[bird_index]
bird_rect = bird_surf.get_rect(center = ((WIDTH / 2) - CENTRAL_OFFSET, 450))
BIRD_FLAP = pygame.USEREVENT
pygame.time.set_timer(BIRD_FLAP, 150)

# Pipes
pipe_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\pipe-green.png').convert_alpha(), (68, 416))
pipe_list = []
col_pipe_list = []
SPAWN_PIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_PIPE, 1000)
pipe_height = [500 ,550, 600, 650]
pipe_cap = [150, 200, 250, 300, 350]

class Game():
    def __init__(self, width, height, fps, gravity, scroll_speed, font_size, central_offset):
        self.width = width
        self.height = height
        self.fps = fps
        self.gravity = gravity
        self.scroll_speed = scroll_speed
        self.font_size = font_size
        self.central_offset = central_offset
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('FlappyBird')
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\04B_19.TTF', self.font_size)

        # Game over message
        self.game_over_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\gameover.png').convert_alpha(), (346, 76))
        self.game_over_rect = self.game_over_surf.get_rect(center = ((self.width / 2, 300)))

        # Sounds
        self.flap_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\wing.wav')
        self.hit_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\hit.wav')
        self.death_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\die.wav')
        self.point_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\point.wav')
        self.swoosh_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\swoosh.wav')

        # Background
        self.bg_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\background-day.png').convert(), (self.width, self.height))
        self.floor_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\base.png').convert(), (self.width, int(self.height / 4)))


class Pipe():
    def __init__(self, x, y, width, height, scroll_speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_speed = scroll_speed
        self.pipe_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\pipe-green.png').convert(), (self.width, self.height))
        self.pipe_rect = self.pipe_surf.get_rect(midtop = (self.x, self.y))

    def move(self):
        self.pipe_rect.centerx -= self.scroll_speed

    def draw(self, screen):
        screen.blit(self.pipe_surf, self.pipe_rect)

    def off_screen(self):
        return self.pipe_rect.right < 0

    def collision(self, bird):
        return bird.bird_rect.colliderect(self.pipe_rect)
    
class Floor():
    def __init__(self, x, y, width, height, scroll_speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_speed = scroll_speed
        self.floor_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\base.png').convert(), (self.width, self.height))
        self.floor_rect = self.floor_surf.get_rect(midtop = (self.x, self.y))

    def move(self):
        self.floor_rect.centerx -= self.scroll_speed

    def draw(self, screen):
        screen.blit(self.floor_surf, self.floor_rect)

    def off_screen(self):
        return self.floor_rect.right < 0
    
class Bird():
    def __init__(self, x, y, width, height, gravity, scroll_speed, central_offset):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gravity = gravity
        self.scroll_speed = scroll_speed
        self.central_offset = central_offset
        self.bird_movement = 0
        self.bird_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-midflap.png').convert_alpha(), (self.width, self.height))
        self.bird_rect = self.bird_surf.get_rect(center = (self.x, self.y))
        self.bird_flap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-midflap.png').convert_alpha(), (self.width, self.height))
        self.bird_flap_rect = self.bird_flap.get_rect(center = (self.x, self.y))
        self.bird_midflap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-midflap.png').convert_alpha(), (self.width, self.height))
        self.bird_midflap_rect = self.bird_midflap.get_rect(center = (self.x, self.y))
        self.bird_downflap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-downflap.png').convert_alpha(), (self.width, self.height))
        self.bird_downflap_rect = self.bird_downflap.get_rect(center = (self.x, self.y))
        self.bird_frames = [self.bird_flap, self.bird_midflap, self.bird_downflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (self.x, self.y))
        self.bird_rotation = 0
        self.bird_rotation_speed = 20

    def move(self):
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

    def draw(self, screen):
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (self.x, self.y))
        screen.blit(self.bird_surface, self.bird_rect)
    
    def flap(self):
        self.bird_movement = 0
        self.bird_movement -= self.central_offset

    def rotate(self):
        self.bird_rotation -= self.bird_rotation_speed
        self.bird_surface = pygame.transform.rotozoom(self.bird_surface, self.bird_rotation, 1)
        self.bird_rect = self.bird_surface.get_rect(center = (self.x, self.y))
    
    def animation(self):
        self.bird_index += 1
        if self.bird_index >= len(self.bird_frames):
            self.bird_index = 0

    def collision(self, floor):
        return self.bird_rect.colliderect(floor.floor_rect)
    

class Score():
    def __init__(self, width, height, font_size, score, high_score):
        self.width = width
        self.height = height
        self.font_size = font_size
        self.score = score
        self.high_score = high_score
        self.score_surf = game_font.render(str(int(self.score)), True, (255, 255, 255))
        self.score_rect = self.score_surf.get_rect(center = (self.width / 2, self.height / 10))
        self.high_score_surf = game_font.render('High Score: ' + str(int(self.high_score)), True, (255, 255, 255))
        self.high_score_rect = self.high_score_surf.get_rect(center = (self.width / 2, self.height / 10))

    def draw(self, screen):
        screen.blit(self.score_surf, self.score_rect)
        screen.blit(self.high_score_surf, self.high_score_rect)

    def update(self):
        self.score_surf = game_font.render(str(int(self.score)), True, (255, 255, 255))
        self.score_rect = self.score_surf.get_rect(center = (self.width / 2, self.height / 10))
        self.high_score_surf = game_font.render('High Score: ' + str(int(self.high_score)), True, (255, 255, 255))
        self.high_score_rect = self.high_score_surf.get_rect(center = (self.width / 2, self.height / 10))

def main():
    # Changeable game variables
    CENTRAL_OFFSET = 60
    FPS = 120
    GRAVITY = 0.25
    SCROLL_SPEED = 4
    FONT_SIZE = 45

    # Game variables
    WIDTH, HEIGHT = 600, 900
    BIRD_MOVEMENT = 0
    SCORE = 0
    HIGH_SCORE = 0
    GAME_ACTIVE = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('FlappyBird')
    clock = pygame.time.Clock()
    game_font = pygame.font.Font('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\04B_19.TTF', FONT_SIZE)

    # Game over message
    game_over_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\message.png').convert_alpha(), (WIDTH, HEIGHT))
    game_over_rect = game_over_surf.get_rect(center = (WIDTH / 2, HEIGHT / 2))

    # Game objects
    bird = Bird(100, HEIGHT / 2, 50, 40, GRAVITY, SCROLL_SPEED, CENTRAL_OFFSET)
    floor = Floor(0, HEIGHT - 100, WIDTH, 100, SCROLL_SPEED)
    pipe = Pipe(WIDTH, HEIGHT, 100, 500, SCROLL_SPEED)
    score = Score(WIDTH, HEIGHT, FONT_SIZE, SCORE, HIGH_SCORE)

    # Game loop
    while True:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and GAME_ACTIVE:
                    bird.flap()
                if event.key == pygame.K_SPACE and not GAME_ACTIVE:
                    GAME_ACTIVE = True
                    pipe.pipe_list.clear()
                    bird.bird_rect.center = (100, HEIGHT / 2)
                    bird.bird_movement = 0
                    score.score = 0

        # Game logic
        if GAME_ACTIVE:
            # Bird
            bird.move()
            bird.animation()
            bird.rotate()
            bird.draw(screen) 
            # Pipe
            pipe.move()
            pipe.draw(screen)
            pipe.collision(bird)
            # Floor
            floor.move()
            floor.draw(screen)
            # Score
            score.score += 0.01
            score.update()
            # Game over
            if bird.collision(floor):
                GAME_ACTIVE = False
                if score.score > score.high_score:
                    score.high_score = score.score

        # Draw
        screen.blit(bg_surf, (0, 0))
        bird.draw(screen)
        score.draw(screen)
        if not GAME_ACTIVE:
            screen.blit(game_over_surf, game_over_rect)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()



# # Changeable game variables
# CENTRAL_OFFSET = 60
# FPS = 120
# GRAVITY = 0.25
# SCROLL_SPEED = 4
# FONT_SIZE = 45

# # Game variables
# WIDTH, HEIGHT = 600, 900
# BIRD_MOVEMENT = 0
# SCORE = 0
# HIGH_SCORE = 0
# GAME_ACTIVE = True
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption('FlappyBird')
# clock = pygame.time.Clock()
# game_font = pygame.font.Font('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\04B_19.TTF', FONT_SIZE)

# # Game over message
# game_over_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\gameover.png').convert_alpha(), (346, 76))
# game_over_rect = game_over_surf.get_rect(center = ((WIDTH / 2, 300)))

# # Sounds
# flap_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\wing.wav')
# hit_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\hit.wav')
# death_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\die.wav')
# point_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\point.wav')
# swoosh_sound = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\sounds\\swoosh.wav')

# # Background
# bg_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\background-day.png').convert(), (WIDTH, HEIGHT))
# floor_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\base.png').convert(), (WIDTH, int(HEIGHT / 4)))
# floor_x = 0

# # Bird
# bird_down_flap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-downflap.png').convert_alpha(), (44, 31))
# bird_mid_flap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-midflap.png').convert_alpha(), (44, 31))
# bird_up_flap = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\bluebird-upflap.png').convert_alpha(), (44, 31))
# bird_frames = [bird_down_flap, bird_mid_flap, bird_up_flap]
# bird_index = 0
# bird_surf = bird_frames[bird_index]
# bird_rect = bird_surf.get_rect(center = ((WIDTH / 2) - CENTRAL_OFFSET, 450))
# BIRD_FLAP = pygame.USEREVENT
# pygame.time.set_timer(BIRD_FLAP, 150) 

# # Pipes
# pipe_surf = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\CODE\\MachineLearning\\FlappyBird - GA\\assets\\visuals\\pipe-green.png').convert_alpha(), (68, 416))
# pipe_list = []
# col_pipe_list = []
# SPAWN_PIPE = pygame.USEREVENT + 1
# pygame.time.set_timer(SPAWN_PIPE, 1000)
# pipe_height = [500 ,550, 600, 650]
# pipe_cap = [150, 200, 250, 300, 350]

# def draw_floor():
#     screen.blit(floor_surf, (floor_x, HEIGHT - 120))
#     screen.blit(floor_surf, (floor_x + WIDTH, HEIGHT - 120))

# def create_pipe():
#     bottom_height = random.choice(pipe_height)
#     bottom_pipe = pipe_surf.get_rect(midtop = (WIDTH + 30, bottom_height))
#     top_height = bottom_height - bottom_pipe.height - random.choice(pipe_cap)

#     if top_height > 0:
#         top_height = -1

#     top_pipe = pipe_surf.get_rect(midtop=(WIDTH + 30, top_height))
#     return bottom_pipe, top_pipe

# def move_pipes(pipes):
#     for pipe in pipes:
#         pipe.centerx -= SCROLL_SPEED
#     return pipes

# def draw_pipes(pipes):
#     for pipe in pipes:
#         if pipe.bottom >= HEIGHT:
#             screen.blit(pipe_surf, pipe)
#         else:
#             flip_pipe = pygame.transform.flip(pipe_surf, False, True)
#             screen.blit(flip_pipe, pipe)


# def check_point(pipes, bird_rect):
#     for pipe in pipes:
#         if pipe.centerx > (WIDTH * 0.32) and pipe.centerx < bird_rect.centerx:
#             return True
 

# def check_col(pipes, bird_rect):
#     for pipe in pipes:
#         if bird_rect.colliderect(pipe):
#             hit_sound.play()
#             return False

#     if bird_rect.top <= -100 or bird_rect.bottom >= (HEIGHT - 120):
#         hit_sound.play()
#         return False
#     return True

# def rotate_bird(bird):
#     new_bird = pygame.transform.rotozoom(bird, -BIRD_MOVEMENT * 3, 1)
#     return new_bird

# def bird_animation():
#     new_bird = bird_frames[bird_index]
#     new_bird_rect = new_bird.get_rect(center = ((WIDTH / 2) - CENTRAL_OFFSET, bird_rect.centery))
#     return new_bird, new_bird_rect

# def score_display(game_state):
#     if game_state == 'main_game':
#         score_label = game_font.render(f'{int(SCORE)}', True, (255, 255, 255))
#         score_rect = score_label.get_rect(center=(WIDTH / 2, 40))
#         screen.blit(score_label, score_rect)
#     if game_state == 'game_over':
#         score_label = game_font.render(f'Score: {int(SCORE)}', True, (255, 255, 255))
#         score_rect = score_label.get_rect(center=(WIDTH / 2, 40))
#         screen.blit(score_label, score_rect)

#         high_score_label = game_font.render(f'High score: {int(HIGH_SCORE)}', True, (255, 255, 255))
#         high_score_rect = high_score_label.get_rect(center=(WIDTH / 2, 750))
#         screen.blit(high_score_label, high_score_rect)

# def update_high_score(SCORE, HIGH_SCORE):
#     if SCORE > HIGH_SCORE:
#         HIGH_SCORE = SCORE
#     return HIGH_SCORE



# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE and GAME_ACTIVE:
#                 flap_sound.play()
#                 BIRD_MOVEMENT = 0
#                 BIRD_MOVEMENT -= 8
#             if event.key == pygame.K_SPACE and not GAME_ACTIVE:
#                 swoosh_sound.play()
#                 GAME_ACTIVE = True
#                 pipe_list.clear()
#                 bird_rect.center = ((WIDTH / 2) - CENTRAL_OFFSET, 450)
#                 BIRD_MOVEMENT = 0
#                 SCORE = 0

#         if event.type == SPAWN_PIPE:
#             pipe_list.extend(create_pipe())

#         if event.type == BIRD_FLAP:
#             if bird_index < 2:
#                 bird_index += 1
#             else:
#                 bird_index = 0
#             bird_surf, bird_rect = bird_animation()
#     screen.blit(bg_surf, (0, 0))

#     if GAME_ACTIVE:
#         # Bird
#         BIRD_MOVEMENT += GRAVITY
#         rotated_bird = rotate_bird(bird_surf)
#         bird_rect.centery += BIRD_MOVEMENT
#         screen.blit(rotated_bird, bird_rect)
#         GAME_ACTIVE = check_col(pipe_list, bird_rect)

#         # Pipes
#         pipe_list = move_pipes(pipe_list)
#         draw_pipes(pipe_list)

#         # Floor
#         floor_x -= SCROLL_SPEED
#         draw_floor()
#         if floor_x <= -WIDTH:
#             floor_x = 0
#         if check_point(pipe_list, bird_rect):
#             SCORE += 0.1
#             point_sound.play()
#             score_display('main_game')
#         else:
#             screen.blit(game_over_surf, game_over_rect)
#             HIGH_SCORE = update_high_score(SCORE, HIGH_SCORE)
#             score_display('game_over')
#         draw_floor()
#         pygame.display.update()
#         clock.tick(FPS)