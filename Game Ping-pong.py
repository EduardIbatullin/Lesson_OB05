import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_SPEED = 5
PADDLE_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пинг-Понг")


# Класс Paddle
class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = PADDLE_SPEED

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


# Класс Ball
class Ball:
    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x, y, radius*2, radius*2)
        self.dx = BALL_SPEED
        self.dy = BALL_SPEED

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.dx = BALL_SPEED
        self.dy = BALL_SPEED


# Класс Game
class Game:
    def __init__(self):
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 15)
        self.left_paddle = Paddle(30, SCREEN_HEIGHT // 2 - 60, 20, 120)
        self.right_paddle = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 60, 20, 120)

    def handle_collision(self):
        if self.ball.rect.colliderect(self.left_paddle.rect) or self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.dx = -self.ball.dx

    def check_score(self):
        if self.ball.rect.left <= 0 or self.ball.rect.right >= SCREEN_WIDTH:
            self.ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        screen.fill(BLACK)
        self.ball.draw(screen)
        self.left_paddle.draw(screen)
        self.right_paddle.draw(screen)

    def update(self):
        self.ball.move()
        self.handle_collision()
        self.check_score()


# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            game.left_paddle.move_up()
        if keys[pygame.K_s]:
            game.left_paddle.move_down()
        if keys[pygame.K_UP]:
            game.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            game.right_paddle.move_down()

        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
