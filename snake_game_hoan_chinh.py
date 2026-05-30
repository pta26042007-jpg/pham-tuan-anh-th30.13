import pygame
import random
import sys

pygame.init()

WIDTH = 720
HEIGHT = 480
BLOCK = 20

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

score_font = pygame.font.SysFont("bahnschrift",25)
game_font = pygame.font.SysFont("bahnschrift",35)

def show_score(score):
    text = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(text,(10,10))

def draw_snake(snake_list):
    for part in snake_list:
        pygame.draw.rect(screen,GREEN,[part[0],part[1],BLOCK,BLOCK])

def spawn_food():
    return (
        random.randrange(0, WIDTH - BLOCK, BLOCK),
        random.randrange(0, HEIGHT - BLOCK, BLOCK)
    )

def move_snake(x,y,x_change,y_change):
    return x + x_change, y + y_change

def game_over(score):
    while True:
        screen.fill(BLACK)
        msg1 = game_font.render("Game Over", True, RED)
        msg2 = score_font.render("C - Play Again | Q - Quit",True,WHITE)
        msg3 = score_font.render("Score: "+str(score),True,WHITE)
        screen.blit(msg1,(WIDTH//2-80, HEIGHT//2-50))
        screen.blit(msg3,(WIDTH//2-50, HEIGHT//2))
        screen.blit(msg2,(WIDTH//2-130, HEIGHT//2+40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_c:
                    main()

def main():
    x = WIDTH//2
    y = HEIGHT//2
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    food_x, food_y = spawn_food()

    score = 0
    speed = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK
                    x_change = 0

        x, y = move_snake(x,y,x_change,y_change)

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_over(score)

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK, BLOCK])

        snake_head = [x,y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for part in snake_list[:-1]:
            if part == snake_head:
                game_over(score)

        draw_snake(snake_list)
        show_score(score)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x, food_y = spawn_food()
            snake_length += 1
            score += 1
            speed += 0.5

        clock.tick(speed)

main()
