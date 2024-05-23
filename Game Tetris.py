import pygame
import sys
import random


# Основной файл игры Tetris
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board(10, 20)  # Инициализация игрового поля размером 10x20
        self.piece = Piece(self.board)  # Создание текущей фигуры
        self.next_piece = Piece(self.board)  # Создание следующей фигуры
        self.drop_time = 0  # Таймер для автоматического падения фигур
        self.game_over = False  # Флаг окончания игры

    def handle_event(self, event):
        # Обработка событий клавиатуры
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.piece.move(-1, 0)  # Движение влево
            elif event.key == pygame.K_RIGHT:
                self.piece.move(1, 0)  # Движение вправо
            elif event.key == pygame.K_DOWN:
                self.piece.move(0, 1)  # Ускорение падения
            elif event.key == pygame.K_UP:
                self.piece.rotate()  # Поворот фигуры

    def update(self):
        # Обновление состояния игры
        if not self.game_over:
            self.drop_time += 1
            if self.drop_time >= 30:  # Каждые 30 кадров фигура падает на одну клетку
                self.drop_time = 0
                if not self.piece.move(0, 1):  # Если фигура не может падать дальше
                    self.board.place_piece(self.piece)  # Размещение фигуры на доске
                    self.piece = self.next_piece  # Переключение на следующую фигуру
                    self.next_piece = Piece(self.board)  # Создание новой следующей фигуры
                    if not self.board.is_valid_position(self.piece.shape_coords()):  # Проверка позиции новой фигуры
                        self.game_over = True  # Если новая фигура не может разместиться, игра окончена

    def draw(self):
        # Отрисовка игры
        self.screen.fill((0, 0, 0))  # Очистка экрана
        self.board.draw(self.screen)  # Отрисовка игрового поля
        self.piece.draw(self.screen)  # Отрисовка текущей фигуры
        if self.game_over:
            # Отрисовка сообщения об окончании игры
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(text, (50, 250))


# Класс для игрового поля
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]  # Инициализация сетки поля

    def place_piece(self, piece):
        # Размещение фигуры на поле
        for x, y in piece.shape_coords():
            self.grid[y][x] = 1  # Заполнение ячеек фигуры в сетке
        self.clear_lines()  # Очистка заполненных линий

    def clear_lines(self):
        # Очистка заполненных линий
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]  # Оставить только незаполненные линии
        new_lines = self.height - len(new_grid)  # Количество очищенных линий
        self.grid = [[0] * self.width for _ in range(new_lines)] + new_grid  # Добавить новые пустые линии сверху

    def is_valid_position(self, shape_coords):
        # Проверка, может ли фигура быть размещена в текущей позиции
        for x, y in shape_coords:
            if x < 0 or x >= self.width or y >= self.height:
                return False  # Выход за границы поля
            if self.grid[y][x] != 0:
                return False  # Столкновение с другой фигурой
        return True

    def draw(self, screen):
        # Отрисовка игрового поля
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, (255, 255, 255), (x*30, y*30, 30, 30))  # Отрисовка заполненных ячеек


# Класс для управления фигурами
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[0, 1, 1], [1, 1, 0]],  # S-shape
    [[1, 1, 0], [0, 1, 1]],  # Z-shape
    [[1, 1, 1, 1]],          # I-shape
    [[1, 1], [1, 1]],        # O-shape
    [[1, 1, 1], [1, 0, 0]],  # L-shape
    [[1, 1, 1], [0, 0, 1]]   # J-shape
]


class Piece:
    def __init__(self, board):
        self.board = board
        self.shape = random.choice(SHAPES)  # Случайный выбор формы фигуры
        self.x = board.width // 2 - len(self.shape[0]) // 2  # Начальная позиция фигуры
        self.y = 0

    def shape_coords(self):
        # Получение координат ячеек фигуры на игровом поле
        coords = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    coords.append((self.x + x, self.y + y))
        return coords

    def move(self, dx, dy):
        # Перемещение фигуры
        self.x += dx
        self.y += dy
        if not self.board.is_valid_position(self.shape_coords()):
            self.x -= dx  # Отмена перемещения при недопустимой позиции
            self.y -= dy
            return False
        return True

    def rotate(self):
        # Поворот фигуры
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        if not self.board.is_valid_position(self.shape_coords()):
            self.shape = [list(row) for row in zip(*self.shape)][::-1]  # Отмена поворота при недопустимой позиции

    def draw(self, screen):
        # Отрисовка фигуры
        for x, y in self.shape_coords():
            pygame.draw.rect(screen, (255, 255, 255), (x*30, y*30, 30, 30))  # Отрисовка ячеек фигуры


# Основной блок для запуска игры
def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 600))  # Установка размера окна
    pygame.display.set_caption("Tetris")  # Заголовок окна
    clock = pygame.time.Clock()  # Создание объекта Clock для управления FPS
    game = Game(screen)  # Создание объекта Game

    while True:
        # Основной игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)  # Обработка событий

        game.update()  # Обновление состояния игры
        game.draw()  # Отрисовка игры
        pygame.display.flip()  # Обновление экрана
        clock.tick(30)  # Установка FPS


if __name__ == "__main__":
    main()
