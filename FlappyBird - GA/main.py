import sys, pygame, random
pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

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

def draw_floor():
    screen.blit(floor_surf, (floor_x, HEIGHT - 120))
    screen.blit(floor_surf, (floor_x + WIDTH, HEIGHT - 120))

def create_pipe():
    bottom_height = random.choice(pipe_height)
    bottom_pipe = pipe_surf.get_rect(midtop = (WIDTH + 30, bottom_height))
    top_height = bottom_height - bottom_pipe.height - random.choice(pipe_cap)

    if top_height > 0:
        top_height = -1

    top_pipe = pipe_surf.get_rect(midtop=(WIDTH + 30, top_height))

    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= SCROLL_SPEED
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_surf, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surf, False, True)
            screen.blit(flip_pipe, pipe)


def check_point(pipes, bird_rect):
    for pipe in pipes:
        if pipe.centerx > (WIDTH * 0.32) and pipe.centerx < bird_rect.centerx:
            return True
 

def check_col(pipes, bird_rect):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= (HEIGHT - 120):
        hit_sound.play()
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -BIRD_MOVEMENT * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = ((WIDTH / 2) - CENTRAL_OFFSET, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_label = game_font.render(f'{int(SCORE)}', True, (255, 255, 255))
        score_rect = score_label.get_rect(center=(WIDTH / 2, 40))
        screen.blit(score_label, score_rect)
    if game_state == 'game_over':
        score_label = game_font.render(f'Score: {int(SCORE)}', True, (255, 255, 255))
        score_rect = score_label.get_rect(center=(WIDTH / 2, 40))
        screen.blit(score_label, score_rect)

        high_score_label = game_font.render(f'High score: {int(HIGH_SCORE)}', True, (255, 255, 255))
        high_score_rect = high_score_label.get_rect(center=(WIDTH / 2, 750))
        screen.blit(high_score_label, high_score_rect)

def update_high_score(SCORE, HIGH_SCORE):
    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE
    return HIGH_SCORE

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and GAME_ACTIVE:
                flap_sound.play()
                BIRD_MOVEMENT = 0
                BIRD_MOVEMENT -= 8
            if event.key == pygame.K_SPACE and not GAME_ACTIVE:
                swoosh_sound.play()
                GAME_ACTIVE = True
                pipe_list.clear()
                bird_rect.center = ((WIDTH / 2) - CENTRAL_OFFSET, 450)
                BIRD_MOVEMENT = 0
                SCORE = 0

        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRD_FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surf, bird_rect = bird_animation()

    screen.blit(bg_surf, (0, 0))

    if GAME_ACTIVE:
        # Bird
        BIRD_MOVEMENT += GRAVITY
        rotated_bird = rotate_bird(bird_surf)
        bird_rect.centery += BIRD_MOVEMENT
        screen.blit(rotated_bird, bird_rect)
        GAME_ACTIVE = check_col(pipe_list, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Floor
        floor_x -= SCROLL_SPEED
        draw_floor()
        if floor_x <= -WIDTH:
            floor_x = 0

        if check_point(pipe_list, bird_rect):
            SCORE += 0.1
            point_sound.play()
        score_display('main_game')
 
    else:
        screen.blit(game_over_surf, game_over_rect)
        HIGH_SCORE = update_high_score(SCORE, HIGH_SCORE)
        score_display('game_over')

    draw_floor()


    pygame.display.update()
    clock.tick(FPS)
