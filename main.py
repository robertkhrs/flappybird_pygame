import pygame
import sys
import random
import os
import math

pygame.init()
FPS = 60

fon = pygame.mixer.Sound("sounds/rdr_fon.wav")
fon.set_volume(0.3)
shot = pygame.mixer.Sound("sounds/shot.wav")

_circle_cache = {}

score = 0
high_score = 0
score_time = True
score_font = pygame.font.SysFont('dellcyrrusbyme', 30, False, True)

width, height = 550, 620
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

back_img = pygame.image.load("background2.png").convert()

bg_width = back_img.get_width()
bg_rect = back_img.get_rect()
tiles2 = math.ceil(width / bg_width) + 1

scroll1 = 0
scroll2 = 0

bird_img = pygame.image.load("bird2.png")
bird_flap = pygame.USEREVENT
bird_rect = bird_img.get_rect(center=(53, 100))
bird_movement = 0
gravity = 0.17

pipe_img = pygame.image.load("pipe2.png")
pipe_height = [400, 350, 533, 490, 367]

pipes = []
create_pipe = pygame.USEREVENT
pygame.time.set_timer(create_pipe, 1200)

game_over = False
over_img = pygame.image.load("fon2.png").convert_alpha()
over_rect = over_img.get_rect(center=(width // 2, height // 2))


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render(text, font, gfcolor=pygame.Color('White'), ocolor=(0, 0, 0), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Flappy Bird",
                  "",
                  "",
                  "          Правила игры и управление:",
                  "        Прыжок - пробел на клавиатуре",
                  "Пролетать между трубами, не врезаясь в них",
                  "",
                  "",
                  "",
                  "",
                  'Press  "SPACE"  to start the game',
                  'Нажмите  "ПРОБЕЛ"  чтобы начать игру'
                  ]

    fon = pygame.transform.scale(load_image('fon2.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('comicsansms', 22, True, False)
    text_coord = 50
    name_of_game_font = pygame.font.SysFont('dellcyrrusbyme', 50, False, True)
    screen.blit(render(intro_text[0], name_of_game_font), (140, 40))
    for line in intro_text[1:]:
        string_rendered = font.render(line, 1, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(render(line, font), intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def create_pipes():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(550, pipe_y - 190))
    bottom_pipe = pipe_img.get_rect(midtop=(550, pipe_y))
    return top_pipe, bottom_pipe


def pipe_animation():
    global game_over, score_time
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)

        pipe.centerx -= 3
        if pipe.right < 0:
            pipes.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True


def draw_score(game_state):
    menu_font = pygame.font.SysFont('comicsansms', 22, True, False)
    if game_state == "game_on":
        screen.blit(render(f'Score: {str(score)}', score_font), (250, 25))
    elif game_state == "game_over":
        screen.blit(render(f'High Score: {str(high_score)}', score_font), (210, 65))
        screen.blit(render(f'    Press "SPACE" to start the game', menu_font), (65, 400))
        screen.blit(render(f'Нажмите "ПРОБЕЛ" чтобы начать игру', menu_font), (65, 450))


def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if 65 < pipe.centerx < 69 and score_time:
                score += 1
                score_time = False
            if pipe.left <= 0:
                score_time = True

    if score > high_score:
        high_score = score


start_screen()
running = True
while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_movement = -5

            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                bird_rect = bird_img.get_rect(center=(53, 100))
                pipes = []
                bird_movement = 0
                score = 0

        if event.type == bird_flap:
            bird_rect = bird_img.get_rect(center=bird_rect.center)

        if event.type == create_pipe:
            pipes.extend(create_pipes())

    for i in range(0, tiles2):
        screen.blit(back_img, (i * bg_width + scroll2, 0))
        bg_rect.x = i * bg_width + scroll2

    # for i in range(0, tiles1):
    #     screen.blit(floor_img, (i * fl_width + scroll1, 550))
    #     fl_rect.x = i * fl_width + scroll1

    scroll1 -= 5
    scroll2 -= 2

    if abs(scroll2) > bg_width:
        scroll2 = 0
    # if abs(scroll1) > fl_width:
    #     scroll1 = 0

    if not game_over:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

        if bird_rect.top < 5 or bird_rect.bottom >= 550:
            game_over = True

        screen.blit(rotated_bird, bird_rect)
        score_update()
        pipe_animation()
        fon.play()
        draw_score("game_on")

    elif game_over:
        fon.stop()
        screen.blit(over_img, over_rect)
        draw_score("game_over")

    pygame.display.update()
pygame.quit()
sys.exit()
