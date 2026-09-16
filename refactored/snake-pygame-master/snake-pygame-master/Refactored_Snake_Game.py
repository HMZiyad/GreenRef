
import pygame, sys, time, random
from collections import deque

# Constants
difficulty = 25
frame_size_x, frame_size_y = 720, 480
block_size = 10

# Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

# Init
pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
fps_controller = pygame.time.Clock()

# Fonts
main_font = pygame.font.SysFont('times new roman', 90)
score_font = pygame.font.SysFont('consolas', 20)

# Game state
snake_pos = [100, 50]
snake_body = deque([[100, 50], [90, 50], [80, 50]])
food_pos = [random.randrange(1, (frame_size_x//block_size)) * block_size,
            random.randrange(1, (frame_size_y//block_size)) * block_size]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

def game_over():
    game_window.fill(BLACK)
    surface = main_font.render('YOU DIED', True, RED)
    rect = surface.get_rect(center=(frame_size_x/2, frame_size_y/4))
    game_window.blit(surface, rect)
    show_score(False)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def show_score(in_game=True):
    surf = score_font.render(f'Score : {score}', True, WHITE)
    rect = surf.get_rect(midtop=(frame_size_x/10, 15) if in_game else (frame_size_x/2, frame_size_y/1.25))
    game_window.blit(surf, rect)

# Direction mapping
key_map = {
    pygame.K_UP: 'UP', pygame.K_DOWN: 'DOWN',
    pygame.K_LEFT: 'LEFT', pygame.K_RIGHT: 'RIGHT',
    ord('w'): 'UP', ord('s'): 'DOWN', ord('a'): 'LEFT', ord('d'): 'RIGHT'
}

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in key_map:
                change_to = key_map[event.key]
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Update direction
    opposites = {'UP':'DOWN', 'DOWN':'UP', 'LEFT':'RIGHT', 'RIGHT':'LEFT'}
    if change_to != opposites.get(direction):
        direction = change_to

    # Move
    if direction == 'UP': snake_pos[1] -= block_size
    elif direction == 'DOWN': snake_pos[1] += block_size
    elif direction == 'LEFT': snake_pos[0] -= block_size
    elif direction == 'RIGHT': snake_pos[0] += block_size

    # Grow or move
    snake_body.appendleft(list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, frame_size_x//block_size)*block_size,
                    random.randrange(1, frame_size_y//block_size)*block_size]
        food_spawn = True

    game_window.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(game_window, GREEN, pygame.Rect(*pos, block_size, block_size))
    pygame.draw.rect(game_window, WHITE, pygame.Rect(*food_pos, block_size, block_size))

    # Game over conditions
    if (snake_pos[0] < 0 or snake_pos[0] >= frame_size_x or
        snake_pos[1] < 0 or snake_pos[1] >= frame_size_y or
        snake_pos in list(snake_body)[1:]):
        game_over()

    show_score(True)
    pygame.display.update()
    fps_controller.tick(difficulty)
