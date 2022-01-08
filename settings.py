class Settings:
    """Класс для хранени явсех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Параметры экрана.
        self.screen_width = 765
        self.screen_height = 765
        self.bg_color = (0, 0, 0)

        # Параметры ячейки вопроса
        self.cell_width = 60
        self.cell_height = 60
        self.cell_indent = 15
        self.cell_color = (255, 255, 255)
        self.empty_cell_color = (21, 32, 229)
        self.questions_limit = 64


        # Параметры кнопок.
        self.start_button = {
            "width": 200,
            "height": 50,
            "button_c": (0, 255, 0),
            "text_c": (255, 255, 255),
            "font_name": None,
            "font_size": 48,
            "centery": self.screen_height // 2
        }
        self.question_button = {
            "width": 6 * (self.cell_width + self.cell_indent) - self.cell_indent,
            "height": self.cell_height,
            "button_c": (0, 200, 64),
            "text_c": (255, 255, 255),
            "font_name": 'timesnewromanpsmt.ttf',
            "font_size": 39,
            "centery": 3.5 * (self.cell_height + self.cell_indent) + 0.5 * self.cell_indent
        }
