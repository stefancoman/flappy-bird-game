import pygame
import random
import sys
import math

pygame.init()

# TODO: add sounds after getting thru a pipe
# TODO: rewrite this with HTML (maybe)

cheat_mode = False  # maybe add cheat keys later (idk why tf u would want to cheat in flappy bird LMAO)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (118, 185, 0)
RED = (255, 99, 71)
YELLOW = (255, 255, 0)

BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_START_X = SCREEN_WIDTH // 4
BIRD_START_Y = SCREEN_HEIGHT // 2


GRAVITY = 0.5
JUMP_STRENGTH = -8

PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 1500

GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("fappy bird!!")
clock = pygame.time.Clock()

font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

bird_y = BIRD_START_Y
# bird_velocity = -999  # testing crash lol
bird_velocity = 0
pipes = []
score = 0
game_state = GAME_STATE_MENU

print("DEBUG:", bird_y, bird_velocity)


def draw_bird(y):
    bird_rect = pygame.Rect(BIRD_START_X, y, BIRD_WIDTH, BIRD_HEIGHT)
    pygame.draw.rect(screen, BLUE, bird_rect, border_radius=5)

def create_pipe():
    min_height = 100
    max_height = SCREEN_HEIGHT - PIPE_GAP - 100
    
    top_pipe_height = random.randint(min_height, max_height)
    
    top_pipe_rect = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, top_pipe_height)
    
    bottom_pipe_rect = pygame.Rect(SCREEN_WIDTH, top_pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - top_pipe_height - PIPE_GAP)
    
    pipes.append([top_pipe_rect, bottom_pipe_rect, False])

def draw_pipes():
    for top_pipe_rect, bottom_pipe_rect, _ in pipes:
        pygame.draw.rect(screen, GREEN, top_pipe_rect, border_radius=5)
        pygame.draw.rect(screen, GREEN, bottom_pipe_rect, border_radius=5)

def move_pipes():
    for pipe_pair in pipes:
        pipe_pair[0].x -= PIPE_SPEED
        pipe_pair[1].x -= PIPE_SPEED
    
    pipes[:] = [pipe_pair for pipe_pair in pipes if pipe_pair[0].right > 0]

# oh god why did I make this
# works for now, don't touch

def check_collision():
    global game_state

    bird_rect = pygame.Rect(BIRD_START_X, bird_y, BIRD_WIDTH, BIRD_HEIGHT)

    if bird_y <= 0 or bird_y + BIRD_HEIGHT >= SCREEN_HEIGHT:
        game_state = GAME_STATE_GAME_OVER
        return True

    for top_pipe_rect, bottom_pipe_rect, _ in pipes:
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            game_state = GAME_STATE_GAME_OVER
            return True
    return False

def update_score():
    global score
    bird_center_x = BIRD_START_X + BIRD_WIDTH / 2

    for pipe_pair in pipes:
        top_pipe_rect, _, passed_by_bird = pipe_pair
        pipe_center_x = top_pipe_rect.x + PIPE_WIDTH / 2

        if bird_center_x > pipe_center_x and not passed_by_bird:
            score += 1
            pipe_pair[2] = True
            break

def reset_game():
    global bird_y, bird_velocity, pipes, score, game_state
    bird_y = BIRD_START_Y
    bird_velocity = 0
    pipes = []
    score = 0
    game_state = GAME_STATE_PLAYING

def draw_menu_screen():
    screen.fill(BLACK)
    title_text = font_large.render("fapping bird", True, WHITE)
    instructions_text = font_small.render("press SPACE to Start", True, WHITE)
    
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    
    screen.blit(title_text, title_rect)
    screen.blit(instructions_text, instructions_rect)
    pygame.display.flip()

def draw_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font_large.render("game over !", True, RED)
    final_score_text = font_medium.render(f"final scoore: {score}", True, YELLOW)
    restart_text = font_small.render("press SPACE to play again", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(final_score_text, final_score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

last_pipe_spawn_time = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == GAME_STATE_MENU:
                    reset_game()
                elif game_state == GAME_STATE_PLAYING:
                    bird_velocity = JUMP_STRENGTH
                elif game_state == GAME_STATE_GAME_OVER:
                    reset_game()

    if game_state == GAME_STATE_MENU:
        draw_menu_screen()
    
    elif game_state == GAME_STATE_PLAYING:
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_spawn_time > PIPE_SPAWN_INTERVAL:
            create_pipe()
            last_pipe_spawn_time = current_time

        move_pipes()
        check_collision()
        update_score()

        screen.fill(BLACK)
        draw_pipes()
        draw_bird(bird_y)
        
        score_text = font_medium.render(f"score: {score}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    elif game_state == GAME_STATE_GAME_OVER:
        draw_game_over_screen()

    clock.tick(FPS)
