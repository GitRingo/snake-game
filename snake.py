import pygame
from enum import Enum
import random
import math
import time

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

clock = pygame.time.Clock()
clock.tick(60)

speed = 20
scale = 20
window_width = 1280 
window_height = 720


pygame.init()
pygame.display.set_caption("Snake")
window = pygame.display.set_mode((window_width, window_height))

font = pygame.font.SysFont("Arial", 18)

refreshrate = pygame.time.Clock()

global snake_position
snake_position = [500,500]
snake_body = [[500, 500], [490, 500], [480, 500]]

food_position = [100, 100]

score = 0

def handle_keys(direction):
    new_direction = direction
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        if event.key == pygame.K_UP and direction != Direction.DOWN:
            new_direction = Direction.UP
        if event.key == pygame.K_DOWN and direction != Direction.UP:
            new_direction = Direction.DOWN
        if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
            new_direction = Direction.RIGHT 
        if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
            new_direction = Direction.LEFT
    return new_direction

def game_loop():
    direction = Direction.RIGHT
    while True:
        direction = handle_keys(direction)
        move_snake(direction)
        eating()
        repaint()
        paint_hud()
        display_fps()
        window.blit(display_fps(), (1000,0))
        clock.tick()
        pygame.display.update()
        refreshrate.tick(speed)
        game_over()

def display_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps,1, pygame.Color("coral"))
    return fps_text

def move_snake(direction):
    if direction == Direction.UP:
        snake_position[1] -= scale
    if direction == Direction.DOWN:
        snake_position[1] += scale
    if direction == Direction.RIGHT:
        snake_position[0] += scale
    if direction == Direction.LEFT:
        snake_position[0] -= scale
    print(snake_position)
    snake_body.insert(0, list(snake_position))

def generate_new_food():
    food_position[0] = random.randint(5,((window_width - 2) // scale)) * scale
    food_position[1] = random.randint(5,((window_height -2) // scale)) * scale 

def eating():
    global score
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 10
        generate_new_food()
    else:
        snake_body.pop()


def repaint():
    window.fill(pygame.Color(226,176,7))
    for body in snake_body:
        pygame.draw.circle(window, pygame.Color(127, 0, 255), (body[0], body[1]), scale/2) #radius am Ende
    pygame.draw.rect(window, pygame.Color(0,128,255), pygame.Rect(food_position[0]-scale/2, food_position[1]-scale/2, scale, scale))

def game_over_message():
    font = pygame.font.SysFont("Arial", scale*4)
    render = font.render(f"Score: {score} ", True, pygame.Color(255,255,255))
    rect = render.get_rect()
    rect.midtop = (window_width / 2, window_height / 2)
    window.blit(render, rect)
    pygame.display.flip()
    time.sleep(2)
    exit(0)
    

def game_over():
    if snake_position[0] < 0 or snake_position[0] > window_width - scale:
        game_over_message()

    if snake_position[1] < 0 or snake_position[1] > window_height - scale:
        game_over_message()

    for i in snake_body[1:]:
        if snake_position[0] == i[0] and snake_position[1] == i[1]:
            game_over_message()

def paint_hud():
    font = pygame.font.SysFont("Arial", scale*2)
    render = font.render(f"Score: {score} ", True, pygame.Color(255,255,255))
    rect = render.get_rect()
    window.blit(render, rect)
    pygame.display.flip()

if __name__ == "__main__":
    game_loop()
