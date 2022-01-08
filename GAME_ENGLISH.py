import pygame
import sys

from questions_cells import Cells
from settings import Settings
from scoreboard import Scoreboard
from game_stats import GameStats
from button import Button
from questions import Question


class EnglishGame:
    """Класс для управления поведением и ресурсами игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        # Создание экрана игры.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("English")

        # Создание экземляра для хранения игровой статистики
        # и статистики результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.questions = Question(self)
        self.cells = pygame.sprite.Group()
        self.empty_cells = pygame.sprite.Group()
        self._create_grid_of_cells()

        # Создание кнопки PLay и кнопки выхода из уровня
        self.play_button = Button(self, self.settings.start_button, "Play")
        self.quit_level_button = Button(self, self.settings.start_button, "Quit level")
        self.quit_level_button.rect.bottom = 8 * (self.settings.cell_height + self.settings.cell_indent)
        self.quit_level_button.msg_image_rect.centery = self.quit_level_button.rect.centery

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            if self.stats.questions_left == 0:
                self.sb.first_game = False
                self.questions = Question(self)
                self.stats.game_active = False

            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_cells_button(mouse_pos)
                self._check_answer_buttons(mouse_pos)
                self._check_quit_level_button(mouse_pos)

    def _quit_game(self):
        """Завершение игры и сохранение результатов."""

        with open("high_score.txt", 'w') as f:
            f.write(str(self.stats.high_score))

        sys.exit()

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            self._quit_game()

    def _start_game(self):
        """Запускает новую игру при нажатии P или кнопки Play."""
        if not self.stats.game_active:
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.stats.question_active = False

            # Очистка всех ячеек.
            self.cells.empty()
            self.empty_cells.empty()

            # Создание ячеек с вопросами.
            self._create_grid_of_cells()

    def _check_cells_button(self, mouse_pos):
        """Проверка нажатия на ячейку с вопросом."""
        if not self.stats.question_active:
            for cell in self.cells:
                if cell.rect.collidepoint(mouse_pos):
                    self.stats.question_active = True
                    self._create_empty_cell(cell)
                    self.cells.remove(cell)
                    self.questions.get_new_question()
                    break

    def _check_answer_buttons(self, mouse_pos):
        """Проверка нажатия на кноку ответа на вопрос."""
        if self.stats.question_active:
            count = 0
            for answer in self.questions.answers:
                if answer.rect.collidepoint(mouse_pos):
                    answer_keys = list(self.questions.answer.keys())
                    self.stats.score += self.questions.answer[answer_keys[count]]
                    self.stats.question_active = False
                    self.stats.questions_left -= 1

                    break
                count += 1

    def _check_quit_level_button(self, mouse_pos):
        """Проверка нажатия на кнопку выхода из уровня."""
        if self.quit_level_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = False
            self.sb.first_game = False

    def _create_grid_of_cells(self):
        """Создание ячеек для вопросов."""
        for row_number in range(10):
            if row_number in (0, 1, 8, 9):
                for cell_number in range(10):
                    self._create_cell(cell_number, row_number)
            else:
                for cell_number in (0, 1, 8, 9):
                    self._create_cell(cell_number, row_number)

    def _create_cell(self, cell_number, row_number):
        """Создание ячейки и размещение ее в ряду."""
        cell = Cells(self)
        cell_width, cell_height = cell.rect.size
        cell.x = self.settings.cell_indent * (1 + cell_number) + cell_number * cell_width
        cell.rect.x = cell.x
        cell.rect.y = self.settings.cell_indent * (1 + row_number) + row_number * cell_height
        self.cells.add(cell)

    def _create_empty_cell(self, cell):
        """Создание пустой ячейки и размещение ее в ряду."""
        empty_cell = Cells(self)
        empty_cell.rect.x = cell.rect.x
        empty_cell.rect.y = cell.rect.y
        self.empty_cells.add(empty_cell)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)

        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.sb.show_stats()
        else:
            for cell in self.cells.sprites():
                cell.draw_cell(self.settings.cell_color)

            for empty_cell in self.empty_cells.sprites():
                empty_cell.draw_cell(self.settings.empty_cell_color)

            if self.stats.question_active:
                self.questions.draw_question()

            self.sb.show_score()
            self.quit_level_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Создание экзмепляра и запуск игры
    eg = EnglishGame()
    eg.run_game()
