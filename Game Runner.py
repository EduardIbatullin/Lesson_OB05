import pygame
import random
import sys

# Константы для экрана, размера игрока, препятствий, дополнительных жизней, монет, алмазов, кадров в секунду и начальных жизней игрока
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
PLAYER_RADIUS = 20
OBSTACLE_SIZE = 40
LIFE_SIZE = 30
COIN_RADIUS = 10
DIAMOND_SIZE = 30
FPS = 10
LIVES = 3

# Определение цветов в формате RGB
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Базовый класс для всех игровых объектов
class GameObject:
    def __init__(self, x, y, width, height, color):
        # Создаем прямоугольник объекта с заданными координатами, шириной и высотой
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color  # Цвет объекта

    def draw(self, screen):
        # Отрисовка прямоугольника на экране
        pygame.draw.rect(screen, self.color, self.rect)


# Класс игрока, наследуемый от GameObject
class Player(GameObject):
    def __init__(self, x, y):
        # Инициализация игрока с заданной позицией и цветом
        super().__init__(x, y, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2, BLUE)
        self.lives = LIVES  # Задание начального количества жизней

    def move(self, dx, dy):
        # Перемещение игрока по горизонтали и вертикали
        self.rect.x += dx
        self.rect.y += dy
        # Ограничение движения игрока в пределах экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        # Отрисовка игрока в виде синего круга
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), PLAYER_RADIUS)


# Класс препятствия, наследуемый от GameObject
class Obstacle(GameObject):
    def __init__(self, x, y):
        # Инициализация препятствия с заданной позицией и цветом
        super().__init__(x, y, OBSTACLE_SIZE, OBSTACLE_SIZE, RED)


# Класс дополнительных жизней, наследуемый от GameObject
class Life(GameObject):
    def __init__(self, x, y):
        # Инициализация дополнительной жизни с заданной позицией и цветом
        super().__init__(x, y, LIFE_SIZE, LIFE_SIZE, GREEN)


# Класс монеты, наследуемый от GameObject
class Coin(GameObject):
    def __init__(self, x, y):
        # Инициализация монеты с заданной позицией и цветом
        super().__init__(x, y, COIN_RADIUS * 2, COIN_RADIUS * 2, YELLOW)

    def draw(self, screen):
        # Отрисовка монеты в виде желтого круга
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), COIN_RADIUS)


# Класс алмаза, наследуемый от GameObject
class Diamond(GameObject):
    def __init__(self, x, y):
        # Инициализация алмаза с заданной позицией и цветом
        super().__init__(x, y, DIAMOND_SIZE, DIAMOND_SIZE, CYAN)

    def draw(self, screen):
        # Отрисовка алмаза в виде ромба
        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.centery),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.left, self.rect.centery)
        ]
        pygame.draw.polygon(screen, self.color, points)


# Основной класс игры
class Game:
    def __init__(self):
        # Инициализация Pygame и создание основных компонентов игры
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Runner")
        self.clock = pygame.time.Clock()  # Создание объекта для контроля времени
        self.font = pygame.font.SysFont(None, 55)  # Задание шрифта для текста
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)  # Создание игрока
        self.obstacles = []  # Список для хранения препятствий
        self.lives = []  # Список для хранения дополнительных жизней
        self.coins = []  # Список для хранения монет
        self.diamonds = []  # Список для хранения алмазов
        self.score = 0  # Начальные очки игрока
        self.paused = False  # Флаг состояния паузы

    # Метод для создания нового препятствия
    def create_obstacle(self):
        x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)  # Случайное положение по горизонтали
        y = -OBSTACLE_SIZE  # Начальная позиция выше верхнего края экрана
        self.obstacles.append(Obstacle(x, y))  # Добавление нового препятствия в список

    # Метод для создания новой дополнительной жизни
    def create_life(self):
        x = random.randint(0, SCREEN_WIDTH - LIFE_SIZE)  # Случайное положение по горизонтали
        y = -LIFE_SIZE  # Начальная позиция выше верхнего края экрана
        self.lives.append(Life(x, y))  # Добавление новой жизни в список

    # Метод для создания новой монеты
    def create_coin(self):
        x = random.randint(0, SCREEN_WIDTH - COIN_RADIUS * 2)  # Случайное положение по горизонтали
        y = -COIN_RADIUS * 2  # Начальная позиция выше верхнего края экрана
        self.coins.append(Coin(x, y))  # Добавление новой монеты в список

    # Метод для создания нового алмаза
    def create_diamond(self):
        x = random.randint(0, SCREEN_WIDTH - DIAMOND_SIZE)  # Случайное положение по горизонтали
        y = -DIAMOND_SIZE  # Начальная позиция выше верхнего края экрана
        self.diamonds.append(Diamond(x, y))  # Добавление нового алмаза в список

    # Метод для проверки столкновений игрока с препятствиями, жизнями, монетами и алмазами
    def check_collisions(self):
        # Проверка столкновений с препятствиями
        for obstacle in self.obstacles[:]:
            if self.player.rect.colliderect(obstacle.rect):
                self.player.lives -= 1  # Уменьшение количества жизней
                self.obstacles.remove(obstacle)  # Удаление препятствия

        # Проверка столкновений с дополнительными жизнями
        for life in self.lives[:]:
            if self.player.rect.colliderect(life.rect):
                self.player.lives += 1  # Увеличение количества жизней
                self.lives.remove(life)  # Удаление дополнительной жизни

        # Проверка столкновений с монетами
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.score += 10  # Увеличение очков
                self.coins.remove(coin)  # Удаление монеты

        # Проверка столкновений с алмазами
        for diamond in self.diamonds[:]:
            if self.player.rect.colliderect(diamond.rect):
                self.score += 50  # Увеличение очков
                self.diamonds.remove(diamond)  # Удаление алмаза

    # Метод для обновления состояния игры
    def update(self):
        # Обновление положения препятствий
        for obstacle in self.obstacles:
            obstacle.rect.y += 5  # Перемещение вниз
            if obstacle.rect.top > SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)  # Удаление препятствий, которые вышли за нижний край экрана

        # Обновление положения дополнительных жизней
        for life in self.lives:
            life.rect.y += 5  # Перемещение вниз
            if life.rect.top > SCREEN_HEIGHT:
                self.lives.remove(life)  # Удаление жизней, которые вышли за нижний край экрана

        # Обновление положения монет
        for coin in self.coins:
            coin.rect.y += 5  # Перемещение вниз
            if coin.rect.top > SCREEN_HEIGHT:
                self.coins.remove(coin)  # Удаление монет, которые вышли за нижний край экрана

        # Обновление положения алмазов
        for diamond in self.diamonds:
            diamond.rect.y += 5  # Перемещение вниз
            if diamond.rect.top > SCREEN_HEIGHT:
                self.diamonds.remove(diamond)  # Удаление алмазов, которые вышли за нижний край экрана

        self.check_collisions()  # Проверка столкновений

        # Случайное создание нового препятствия
        if random.random() < 0.02:
            self.create_obstacle()

        # Случайное создание новой дополнительной жизни
        if random.random() < 0.01:
            self.create_life()

        # Случайное создание новой монеты
        if random.random() < 0.03:
            self.create_coin()

        # Случайное создание нового алмаза
        if random.random() < 0.005:
            self.create_diamond()

    # Метод для отрисовки объектов на экране
    def draw(self):
        self.screen.fill(WHITE)  # Заполнение фона белым цветом
        self.player.draw(self.screen)  # Отрисовка игрока
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)  # Отрисовка каждого препятствия
        for life in self.lives:
            life.draw(self.screen)  # Отрисовка каждой дополнительной жизни
        for coin in self.coins:
            coin.draw(self.screen)  # Отрисовка каждой монеты
        for diamond in self.diamonds:
            diamond.draw(self.screen)  # Отрисовка каждого алмаза
        self.draw_lives()  # Отрисовка количества жизней
        self.draw_score()  # Отрисовка текущих очков
        pygame.display.flip()  # Обновление экрана

    # Метод для отрисовки количества жизней игрока
    def draw_lives(self):
        lives_text = self.font.render(f'Жизни: {self.player.lives}', True, BLACK)  # Создание текста с количеством жизней
        self.screen.blit(lives_text, (10, 10))  # Отображение текста в левом верхнем углу

    # Метод для отрисовки текущих очков
    def draw_score(self):
        score_text = self.font.render(f'Очки: {self.score}', True, BLACK)  # Создание текста с текущими очками
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 10))  # Отображение текста в правом верхнем углу

    # Метод для отображения главного меню
    def show_menu(self):
        self.screen.fill(BLACK)  # Заполнение фона черным цветом
        start_text = self.font.render("Начать игру", True, WHITE)  # Текст для начала игры
        quit_text = self.font.render("Выйти из игры", True, WHITE)  # Текст для выхода из игры
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()  # Обновление экрана

    # Метод для отображения меню паузы
    def show_pause_menu(self):
        self.screen.fill(BLACK)  # Заполнение фона черным цветом
        new_game_text = self.font.render("Начать новую игру", True, WHITE)  # Текст для новой игры
        continue_text = self.font.render("Продолжить игру", True, WHITE)  # Текст для продолжения игры
        quit_text = self.font.render("Выйти из игры", True, WHITE)  # Текст для выхода из игры
        self.screen.blit(new_game_text, (SCREEN_WIDTH // 2 - new_game_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        pygame.display.flip()  # Обновление экрана

    # Метод для отображения меню окончания игры
        # Метод для отображения меню окончания игры
    def show_game_over_menu(self):
        self.screen.fill(BLACK)  # Заполнение фона черным цветом
        game_over_text = self.font.render("Конец игры", True, WHITE)  # Текст "Игра окончена"
        score_text = self.font.render(f'Ваши очки: {self.score}', True, WHITE)  # Текст для отображения очков
        new_game_text = self.font.render("Начать новую игру", True, WHITE)  # Текст для новой игры
        quit_text = self.font.render("Завершить игру", True, WHITE)  # Текст для завершения игры

        # Расположение текста на экране
        text_y = SCREEN_HEIGHT // 2 - 50
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, text_y - 150))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, text_y - 50))
        self.screen.blit(new_game_text, (SCREEN_WIDTH // 2 - new_game_text.get_width() // 2, text_y + 50))
        self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, text_y + 100))
        pygame.display.flip()  # Обновление экрана

    # Основной игровой цикл
    def run(self):
        # Отображение главного меню перед началом игры
        in_menu = True
        while in_menu:
            self.show_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        mouse_pos = event.pos
                        # Проверка нажатий на элементы меню
                        if SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100:
                            if SCREEN_HEIGHT // 2 - 100 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 - 50:
                                in_menu = False
                            elif SCREEN_HEIGHT // 2 + 50 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 100:
                                pygame.quit()
                                sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        in_menu = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        running = True  # Флаг для основного игрового цикла
        while running:
            self.clock.tick(FPS)  # Ограничение количества кадров в секунду
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True  # Установка флага паузы
                        while self.paused:
                            self.show_pause_menu()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                    self.paused = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    if event.button == 1:  # Левая кнопка мыши
                                        mouse_pos = event.pos
                                        # Проверка нажатий на элементы меню паузы
                                        if SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100:
                                            if SCREEN_HEIGHT // 2 - 100 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 - 50:
                                                self.__init__()
                                                self.run()
                                            elif SCREEN_HEIGHT // 2 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 50:
                                                self.paused = False
                                            elif SCREEN_HEIGHT // 2 + 100 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 150:
                                                running = False
                                                self.paused = False
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        self.__init__()
                                        self.run()
                                    elif event.key == pygame.K_c:
                                        self.paused = False
                                    elif event.key == pygame.K_q:
                                        running = False
                                        self.paused = False

            keys = pygame.key.get_pressed()
            # Обработка нажатий клавиш для движения игрока
            if keys[pygame.K_LEFT]:
                self.player.move(-5, 0)
            if keys[pygame.K_RIGHT]:
                self.player.move(5, 0)

            self.update()  # Обновление состояния игры
            self.draw()  # Отрисовка объектов на экране

            # Проверка количества жизней игрока
            if self.player.lives <= 0:
                self.paused = True
                while self.paused:
                    self.show_game_over_menu()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            self.paused = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Левая кнопка мыши
                                mouse_pos = event.pos
                                # Проверка нажатий на элементы меню окончания игры
                                if SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100:
                                    if SCREEN_HEIGHT // 2 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 50:
                                        self.__init__()
                                        self.run()
                                    elif SCREEN_HEIGHT // 2 + 50 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 100:
                                        running = False
                                        self.paused = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                self.__init__()
                                self.run()
                            elif event.key == pygame.K_q:
                                running = False
                                self.paused = False


if __name__ == "__main__":
    game = Game()
    game.run()
