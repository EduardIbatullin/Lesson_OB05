import pygame
import sys
import random

# Константы для определения различных состояний игры
MAIN_MENU = 0
PAUSE_MENU = 1
PLAYING = 2
GAME_OVER_MENU = 3


# Класс Settings отвечает за хранение настроек игры
class Settings:
    def __init__(self):
        self.screen_width = 800  # Ширина экрана
        self.screen_height = 600  # Высота экрана
        self.bg_color = (0, 0, 0)  # Цвет фона (черный)
        self.snake_color = (0, 255, 0)  # Цвет змейки (зеленый)
        self.food_color = (255, 0, 0)  # Цвет еды (красный)
        self.segment_size = 20  # Размер сегмента змейки
        self.fps = 15  # Частота кадров


# Класс Snake отвечает за управление змейкой
class Snake:
    def __init__(self, settings):
        self.settings = settings
        # Изначально змейка состоит из одного сегмента, расположенного в центре экрана
        self.segments = [pygame.Rect(settings.screen_width // 2, settings.screen_height // 2, settings.segment_size, settings.segment_size)]
        self.direction = 'RIGHT'  # Начальное направление движения змейки
        self.grow = False  # Флаг, указывающий на необходимость увеличения змейки

    def update(self):
        # Увеличиваем змейку, если флаг grow установлен
        if self.grow:
            self.segments.append(self.segments[-1].copy())
            self.grow = False

        # Перемещаем каждый сегмент змейки на место предыдущего сегмента
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].x = self.segments[i-1].x
            self.segments[i].y = self.segments[i-1].y

        # Перемещаем голову змейки в зависимости от текущего направления
        if self.direction == 'UP':
            self.segments[0].y -= self.settings.segment_size
        elif self.direction == 'DOWN':
            self.segments[0].y += self.settings.segment_size
        elif self.direction == 'LEFT':
            self.segments[0].x -= self.settings.segment_size
        elif self.direction == 'RIGHT':
            self.segments[0].x += self.settings.segment_size

        # Проверяем столкновения
        self._check_collisions()

        # Проверяем выход змейки за границы экрана и перемещаем ее на противоположную сторону
        self._wrap_around_screen()

    def change_direction(self, direction):
        # Избегаем движения в противоположную сторону
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if direction != opposite_directions[self.direction]:
            self.direction = direction

    def draw(self, screen):
        # Отрисовываем каждый сегмент змейки
        for segment in self.segments:
            pygame.draw.rect(screen, self.settings.snake_color, segment)

    def grow_snake(self):
        # Устанавливаем флаг увеличения змейки
        self.grow = True

    def _check_collisions(self):
        head = self.segments[0]
        # Проверяем столкновение головы змейки с ее телом
        for segment in self.segments[1:]:
            if head.colliderect(segment):
                return True
        return False

    def _wrap_around_screen(self):
        head = self.segments[0]
        # Перемещаем змейку на противоположную сторону экрана при выходе за границы
        if head.x < 0:
            head.x = self.settings.screen_width - self.settings.segment_size
        elif head.x >= self.settings.screen_width:
            head.x = 0
        elif head.y < 0:
            head.y = self.settings.screen_height - self.settings.segment_size
        elif head.y >= self.settings.screen_height:
            head.y = 0


# Класс Food отвечает за управление едой
class Food:
    def __init__(self, settings, snake):
        self.settings = settings
        self.rect = pygame.Rect(0, 0, settings.segment_size, settings.segment_size)
        self.snake = snake
        self._place_food()  # Размещаем еду на случайной позиции

    def _place_food(self):
        # Размещаем еду на случайной позиции
        self.rect.x = random.randint(0, (self.settings.screen_width // self.settings.segment_size) - 1) * self.settings.segment_size
        self.rect.y = random.randint(0, (self.settings.screen_height // self.settings.segment_size) - 1) * self.settings.segment_size

    def update(self, snake):
        # Проверяем, съела ли змейка еду
        if snake.segments[0].colliderect(self.rect):
            snake.grow_snake()  # Увеличиваем змейку
            self._place_food()  # Размещаем новую еду

    def draw(self, screen):
        # Отрисовываем еду
        pygame.draw.rect(screen, self.settings.food_color, self.rect)


# Класс Menu отвечает за отображение и обработку меню
class Menu:
    def __init__(self, screen, options, font_size=36):
        self.screen = screen
        self.options = options
        self.font = pygame.font.Font(None, font_size)
        self.selected_option = 0

    def draw(self):
        # Отрисовываем меню на экране
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 50))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def handle_event(self, event):
        # Обрабатываем события в меню
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_option
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i, option in enumerate(self.options):
                text = self.font.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 50))
                if text_rect.collidepoint(mouse_pos):
                    return i
        return None


# Класс Game отвечает за управление игрой
class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Snake Game")

        self.snake = Snake(self.settings)
        self.food = Food(self.settings, self.snake)
        self.clock = pygame.time.Clock()
        self.state = MAIN_MENU

        self.main_menu = Menu(self.screen, ["Start Game", "Quit"])
        self.pause_menu = Menu(self.screen, ["New Game", "Continue", "Quit"])
        self.game_over_menu = Menu(self.screen, ["New Game", "Quit"])

    def run_game(self):
        # Основной игровой цикл
        while True:
            if self.state == MAIN_MENU:
                self._run_main_menu()
            elif self.state == PLAYING:
                self._run_playing()
            elif self.state == PAUSE_MENU:
                self._run_pause_menu()
            elif self.state == GAME_OVER_MENU:
                self._run_game_over_menu()

    def _run_main_menu(self):
        # Запуск главного меню
        self.main_menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            selected_option = self.main_menu.handle_event(event)
            if selected_option is not None:
                if selected_option == 0:  # Start Game
                    self.snake = Snake(self.settings)
                    self.food = Food(self.settings, self.snake)
                    self.state = PLAYING
                elif selected_option == 1:  # Quit
                    pygame.quit()
                    sys.exit()

    def _run_pause_menu(self):
        # Запуск меню паузы
        self.pause_menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            selected_option = self.pause_menu.handle_event(event)
            if selected_option is not None:
                if selected_option == 0:  # New Game
                    self.snake = Snake(self.settings)
                    self.food = Food(self.settings, self.snake)
                    self.state = PLAYING
                elif selected_option == 1:  # Continue
                    self.state = PLAYING
                elif selected_option == 2:  # Quit
                    pygame.quit()
                    sys.exit()

    def _run_game_over_menu(self):
        # Запуск меню при окончании игры
        self.game_over_menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            selected_option = self.game_over_menu.handle_event(event)
            if selected_option is not None:
                if selected_option == 0:  # New Game
                    self.snake = Snake(self.settings)
                    self.food = Food(self.settings, self.snake)
                    self.state = PLAYING
                elif selected_option == 1:  # Quit
                    pygame.quit()
                    sys.exit()

    def _run_playing(self):
        # Запуск игрового процесса
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = PAUSE_MENU
                else:
                    self._check_keydown_events(event)

        self.snake.update()
        self.food.update(self.snake)
        if self.snake._check_collisions():
            self.state = GAME_OVER_MENU

        self._update_screen()
        self.clock.tick(self.settings.fps)

    def _check_keydown_events(self, event):
        # Обрабатываем нажатия клавиш для изменения направления движения змейки
        if event.key == pygame.K_UP:
            self.snake.change_direction('UP')
        elif event.key == pygame.K_DOWN:
            self.snake.change_direction('DOWN')
        elif event.key == pygame.K_LEFT:
            self.snake.change_direction('LEFT')
        elif event.key == pygame.K_RIGHT:
            self.snake.change_direction('RIGHT')

    def _update_screen(self):
        # Обновляем содержимое экрана
        self.screen.fill(self.settings.bg_color)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        pygame.display.flip()


# Точка входа в программу
if __name__ == '__main__':
    game = Game()
    game.run_game()
