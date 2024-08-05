import pygame
import sys

# Инициализация Pygame, необходимая для использования всех функций библиотеки
pygame.init()

# Константы для размеров экрана, скоростей мяча и ракеток, и цветов
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Размеры экрана
BALL_SPEED = 5  # Скорость мяча
PADDLE_SPEED = 10  # Скорость ракеток
WHITE = (255, 255, 255)  # Белый цвет в RGB
BLACK = (0, 0, 0)  # Черный цвет в RGB

# Создание окна для отображения игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пинг-Понг")  # Название окна


# Класс Paddle для управления ракетками
class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # Создание прямоугольника для ракетки
        self.speed = PADDLE_SPEED  # Установка скорости ракетки

    # Метод для перемещения ракетки вверх
    def move_up(self):
        if self.rect.top > 0:  # Проверка, чтобы ракетка не вышла за верхнюю границу экрана
            self.rect.y -= self.speed  # Перемещение ракетки вверх

    # Метод для перемещения ракетки вниз
    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:  # Проверка, чтобы ракетка не вышла за нижнюю границу экрана
            self.rect.y += self.speed  # Перемещение ракетки вниз

    # Метод для отрисовки ракетки на экране
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)  # Отрисовка ракетки в виде белого прямоугольника


# Класс Ball для управления мячом
class Ball:
    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x, y, radius*2, radius*2)  # Создание прямоугольника для мяча
        self.dx = BALL_SPEED  # Скорость мяча по горизонтали
        self.dy = BALL_SPEED  # Скорость мяча по вертикали

    # Метод для перемещения мяча
    def move(self):
        self.rect.x += self.dx  # Перемещение мяча по горизонтали
        self.rect.y += self.dy  # Перемещение мяча по вертикали

        # Проверка столкновения мяча с верхней или нижней границей экрана
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy = -self.dy  # Изменение направления движения по вертикали

    # Метод для отрисовки мяча на экране
    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)  # Отрисовка мяча в виде белого эллипса

    # Метод для сброса позиции мяча к центру экрана
    def reset(self, x, y):
        self.rect.x = x  # Установка новой позиции по горизонтали
        self.rect.y = y  # Установка новой позиции по вертикали
        self.dx = BALL_SPEED  # Сброс скорости мяча по горизонтали
        self.dy = BALL_SPEED  # Сброс скорости мяча по вертикали


# Класс Game для управления всей игрой
class Game:
    def __init__(self):
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 15)  # Создание мяча в центре экрана
        self.left_paddle = Paddle(30, SCREEN_HEIGHT // 2 - 60, 20, 120)  # Создание левой ракетки
        self.right_paddle = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 60, 20, 120)  # Создание правой ракетки

    # Метод для обработки столкновений мяча с ракетками
    def handle_collision(self):
        # Проверка, сталкивается ли мяч с любой из ракеток
        if self.ball.rect.colliderect(self.left_paddle.rect) or self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.dx = -self.ball.dx  # Изменение направления движения по горизонтали

    # Метод для проверки, забит ли гол (мяч вышел за границу экрана)
    def check_score(self):
        if self.ball.rect.left <= 0 or self.ball.rect.right >= SCREEN_WIDTH:  # Мяч вышел за левую или правую границу
            self.ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Сброс мяча в центр экрана

    # Метод для отрисовки всех элементов игры
    def draw(self):
        screen.fill(BLACK)  # Заполнение экрана черным цветом
        self.ball.draw(screen)  # Отрисовка мяча
        self.left_paddle.draw(screen)  # Отрисовка левой ракетки
        self.right_paddle.draw(screen)  # Отрисовка правой ракетки

    # Метод для обновления состояния игры
    def update(self):
        self.ball.move()  # Перемещение мяча
        self.handle_collision()  # Обработка столкновений
        self.check_score()  # Проверка, забит ли гол


# Основной игровой цикл
def main():
    clock = pygame.time.Clock()  # Создание объекта для контроля времени
    game = Game()  # Создание объекта игры

    while True:  # Бесконечный цикл для работы игры
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Если событие - выход из игры
                pygame.quit()  # Завершение работы Pygame
                sys.exit()  # Выход из программы

        # Проверка нажатых клавиш для управления ракетками
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            game.left_paddle.move_up()  # Перемещение левой ракетки вверх
        if keys[pygame.K_s]:
            game.left_paddle.move_down()  # Перемещение левой ракетки вниз
        if keys[pygame.K_UP]:
            game.right_paddle.move_up()  # Перемещение правой ракетки вверх
        if keys[pygame.K_DOWN]:
            game.right_paddle.move_down()  # Перемещение правой ракетки вниз

        game.update()  # Обновление состояния игры
        game.draw()  # Отрисовка всех элементов игры

        pygame.display.flip()  # Обновление содержимого экрана
        clock.tick(60)  # Установка частоты кадров (60 FPS)


# Запуск игры
if __name__ == "__main__":
    main()  # Вызов основного игрового цикла
