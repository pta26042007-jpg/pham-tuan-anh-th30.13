import pygame
import random
import sys

pygame.init()


class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [
            [100, 50],
            [90, 50],
            [80, 50]
        ]
        self.direction = "RIGHT"
        self.change_to = self.direction

    def change_direction(self):
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def move(self, grow=False):
        if self.direction == "UP":
            self.position[1] -= 10
        elif self.direction == "DOWN":
            self.position[1] += 10
        elif self.direction == "LEFT":
            self.position[0] -= 10
        elif self.direction == "RIGHT":
            self.position[0] += 10

        self.body.insert(0, list(self.position))

        if not grow:
            self.body.pop()

    def draw(self, game_window):
        for block in self.body:
            pygame.draw.rect(
                game_window,
                (0, 255, 0),
                pygame.Rect(block[0], block[1], 10, 10)
            )

    def check_self_collision(self):
        for block in self.body[1:]:
            if self.position == block:
                return True
        return False


class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = [0, 0]
        self.spawn([])

    def spawn(self, snake_body):
        while True:
            self.position = [
                random.randrange(1, self.width // 10) * 10,
                random.randrange(1, self.height // 10) * 10
            ]
            if self.position not in snake_body:
                break

    def draw(self, game_window):
        pygame.draw.rect(
            game_window,
            (255, 0, 0),
            pygame.Rect(self.position[0], self.position[1], 10, 10)
        )


class Game:
    def __init__(self):
        self.width = 720
        self.height = 480
        self.speed = 15
        self.score = 0

        self.game_window = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption("Snake Game - Python Pygame")

        self.fps = pygame.time.Clock()

        self.snake = Snake()
        self.food = Food(self.width, self.height)

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)

    def show_score(self):
        score_font = pygame.font.SysFont("times new roman", 25)
        score_surface = score_font.render(
            f"Score : {self.score}",
            True,
            self.white
        )
        self.game_window.blit(score_surface, (10, 10))

    def game_over(self):
        font = pygame.font.SysFont("times new roman", 50)

        while True:
            self.game_window.fill(self.black)

            game_over_surface = font.render(
                "GAME OVER",
                True,
                self.red
            )

            info_font = pygame.font.SysFont(
                "times new roman",
                25
            )

            info_surface = info_font.render(
                "Nhan R de choi lai | ESC de thoat",
                True,
                self.white
            )

            score_surface = info_font.render(
                f"Diem cua ban: {self.score}",
                True,
                self.white
            )

            rect = game_over_surface.get_rect()
            rect.midtop = (self.width / 2, 80)

            self.game_window.blit(
                game_over_surface,
                rect
            )

            self.game_window.blit(
                score_surface,
                (250, 180)
            )

            self.game_window.blit(
                info_surface,
                (170, 250)
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.main()

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def check_collision(self):
        if (
            self.snake.position[0] < 0 or
            self.snake.position[0] >= self.width or
            self.snake.position[1] < 0 or
            self.snake.position[1] >= self.height
        ):
            return True

        if self.snake.check_self_collision():
            return True

        return False

    def main(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.snake.change_to = "UP"

                    elif event.key == pygame.K_DOWN:
                        self.snake.change_to = "DOWN"

                    elif event.key == pygame.K_LEFT:
                        self.snake.change_to = "LEFT"

                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_to = "RIGHT"

            self.snake.change_direction()

            grow = False

            if self.snake.position == self.food.position:
                self.score += 10
                grow = True
                self.food.spawn(self.snake.body)

            self.snake.move(grow)

            if self.check_collision():
                self.game_over()

            self.game_window.fill(self.black)

            self.snake.draw(self.game_window)
            self.food.draw(self.game_window)
            self.show_score()

            pygame.display.update()
            self.fps.tick(self.speed)


if __name__ == "__main__":
    game = Game()
    game.main()