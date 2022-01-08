import pygame.font
from pygame.sprite import Group


class Scoreboard:
    """Класс для вывода игровой информации."""

    def __init__(self, eg_game):
        """Инициализируем атрибуты подсчета очков."""
        self.eg_game = eg_game
        self.screen = eg_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = eg_game.settings
        self.stats = eg_game.stats

        self.first_game = True

        # Настройки шрифта для вывода счета.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

    def prep_images(self):
        """Функция подготовки изображений перед обновлением экрана."""
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        score_str = f"Your score: {self.stats.score}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Вывод счета выше кноки Play.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = self.screen_rect.center
        self.score_rect.centery -= 50

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score_str = f"Your record: {self.stats.high_score}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # Рекорд выводится выше предыдущего счета.
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.center = self.screen_rect.center
        self.high_score_image_rect.centery -= 90

    def show_stats(self):
        """Выводит очки, уровень и количество кораблей на экран."""

        # Проверяет, появится ли новый рекорд.
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score

        # Подготовка изображений счетов.
        self.prep_images()

        if not self.first_game:
            self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)

    def show_score(self):
        """Вывод счета во время игры."""

        self.prep_score()
        self.score_rect.bottom = 3 * (self.settings.cell_indent + self.settings.cell_height)
        self.screen.blit(self.score_image, self.score_rect)
