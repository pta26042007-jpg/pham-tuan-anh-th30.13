import pygame
import random
import sys

pygame.init()

# Kích thước màn hình
WIDTH = 720
HEIGHT = 480
BLOCK = 20

# Màu sắc
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Tạo màn hình game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font chữ
score_font = pygame.font.SysFont("bahnschrift", 25)
game_font = pygame.font.SysFont("bahnschrift", 35)


# Hiển thị điểm số
def show_score(score):
    text = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))


# Vẽ rắn
def draw_snake(snake_list):
    for part in snake_list:
        pygame.draw.rect(screen, GREEN, [part[0], part[1], BLOCK, BLOCK])


# Sinh mồi ngẫu nhiên
def spawn_food(snake_list):
    while True:
        food_x = random.randrange(0, WIDTH - BLOCK, BLOCK)
        food_y = random.randrange(0, HEIGHT - BLOCK, BLOCK)

        if [food_x, food_y] not in snake_list:
            return food_x, food_y


# Di chuyển rắn
def move_snake(x, y, x_change, y_change):
    return x + x_change, y + y_change


# Màn hình game over
def game_over(score):
    while True:
        screen.fill(BLACK)

        msg1 = game_font.render("Game Over", True, RED)
        msg2 = score_font.render("C - Play Again | Q - Quit", True, WHITE)
        msg3 = score_font.render("Score: " + str(score), True, WHITE)

        screen.blit(msg1, (WIDTH // 2 - 90, HEIGHT // 2 - 60))
        screen.blit(msg3, (WIDTH // 2 - 50, HEIGHT // 2 - 10))
        screen.blit(msg2, (WIDTH // 2 - 145, HEIGHT // 2 + 30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_c:
                    return True


# Hàm chính của game
def main():
    while True:
        x = WIDTH // 2
        y = HEIGHT // 2

        x_change = 0
        y_change = 0

        snake_list = []
        snake_length = 1

        score = 0
        speed = 10

        food_x, food_y = spawn_food(snake_list)

        game_running = True

        while game_running:

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    # Không cho quay đầu trực tiếp
                    if event.key == pygame.K_LEFT and x_change == 0:
                        x_change = -BLOCK
                        y_change = 0

                    elif event.key == pygame.K_RIGHT and x_change == 0:
                        x_change = BLOCK
                        y_change = 0

                    elif event.key == pygame.K_UP and y_change == 0:
                        x_change = 0
                        y_change = -BLOCK

                    elif event.key == pygame.K_DOWN and y_change == 0:
                        x_change = 0
                        y_change = BLOCK

            # Di chuyển rắn
            x, y = move_snake(x, y, x_change, y_change)

            # Kiểm tra va tường
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                game_running = False
                break

            # Vẽ nền và mồi
            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK, BLOCK])

            # Tạo đầu rắn
            snake_head = [x, y]
            snake_list.append(snake_head)

            # Giữ đúng chiều dài
            if len(snake_list) > snake_length:
                del snake_list[0]

            # Kiểm tra cắn vào thân
            for part in snake_list[:-1]:
                if part == snake_head:
                    game_running = False
                    break

            draw_snake(snake_list)
            show_score(score)
            pygame.display.update()

            # Ăn mồi
            if x == food_x and y == food_y:
                snake_length += 1
                score += 1
                speed += 0.5
                food_x, food_y = spawn_food(snake_list)

            clock.tick(speed)

        # Game over và lựa chọn
        play_again = game_over(score)

        if not play_again:
            pygame.quit()
            sys.exit()


# Chạy game
main()
