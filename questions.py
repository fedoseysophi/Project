import pygame.font
import json
from random import choice

from button import Button


class Question:
    """Класс для задавания вопроса и вариантов ответа на него. """

    def __init__(self, eg_game):
        self._import_questions()
        self.eg_game = eg_game

    def _import_questions(self):
        """Получаем словарь вопросов с ответами."""
        with open("questions.json", "r", encoding="utf-8") as read_file:
            self.remaining_questions = json.load(read_file)

    def get_new_question(self):
        """Создаем новый вопрос с ответами на него."""
        self._get_msg()
        self.questions = []
        if len(self.question) > 34:
            two_lines = self._get_two_lines(self.question, 34)
            self._add_two_lines(self.eg_game, two_lines, True)
        else:
            self.questions.append(Button(self.eg_game, self.eg_game.settings.question_button, self.question))
        self.answers = []
        self.second_lines_answers = []
        self._set_buttons(self.eg_game)

    def _get_msg(self):
        """Получаем рандомный вопрос из списка."""
        self.question = choice(list(self.remaining_questions))
        self.answer = self.remaining_questions[self.question]
        del self.remaining_questions[self.question]

    def _set_buttons(self, eg_game):
        """Создаем 3 кнопки для ответов."""
        count = 0
        answers = list(self.answer.keys())

        for abc in ('a', 'b', 'c'):
            if len(answers[count]) > 27:
                two_lines = self._get_two_lines(answers[count], 27)
                count += 1
                self._add_two_lines(eg_game, two_lines, False, abc, count)
            else:
                self.answers.append(Button(eg_game, eg_game.settings.question_button,
                                           f"{abc}) {answers[count]}"))
                count += 1
                self.answers[-1].rect.centery += (self.eg_game.settings.cell_height +
                                                  self.eg_game.settings.cell_indent) * count
                self.answers[-1].msg_image_rect.centery = self.answers[-1].rect.centery
                self.answers[-1].msg_image_rect.x = (self.eg_game.settings.screen_width -
                                           self.eg_game.settings.question_button["width"]) / 2 + 5

    def _get_two_lines(self, str, len_line):
        """Разделение предложения на две строки."""
        str_list = str.split()
        len_str = 0
        line1 = ""
        line2 = ""

        i = 0
        for word in str_list:
            len_str += len(word) + 1
            if i == 0:
                len_str -= 1
            i += 1

            if len_str > len_line:
                for k in range(i - 1):
                    line1 += str_list[k] + " "
                for k in range(i - 1, len(str_list)):
                    line2 += str_list[k] + " "
                break

        return line1, line2

    def _add_two_lines(self, eg_game, lines, que_or_ans, abc='', count=0):
        """Создание 2 строк одной кнопоки."""
        if que_or_ans:
            eg_game.settings.question_button["font_size"] = 30
            self.questions.append(Button(eg_game, eg_game.settings.question_button,
                                       f"{lines[0][:-1]}"))
            self.questions[-1].msg_image_rect.centery -= 12
            self.questions[-1].msg_image_rect.x = (self.eg_game.settings.screen_width -
                                                 self.eg_game.settings.question_button["width"]) / 2 + 5

            self.questions.append(Button(eg_game, eg_game.settings.question_button,
                                                    f"{lines[1][:-1]}"))
            self.questions[-1].rect.centery += 1000
            self.questions[-1].msg_image_rect.centery = self.questions[-2].msg_image_rect.centery + 25
            self.questions[-1].msg_image_rect.x = self.questions[-2].msg_image_rect.x
        else:
            eg_game.settings.question_button["font_size"] = 35
            self.answers.append(Button(eg_game, eg_game.settings.question_button,
                                        f"{abc}) {lines[0][:-1]}"))
            self.answers[-1].rect.centery += (self.eg_game.settings.cell_height +
                                              self.eg_game.settings.cell_indent) * count
            self.answers[-1].msg_image_rect.centery = self.answers[-1].rect.centery - 12
            self.answers[-1].msg_image_rect.x = (self.eg_game.settings.screen_width -
                                                 self.eg_game.settings.question_button["width"]) / 2 + 5

            self.second_lines_answers.append(Button(eg_game, eg_game.settings.question_button,
                                       f"{lines[1][:-1]}"))
            self.second_lines_answers[-1].rect.centery += 1000
            self.second_lines_answers[-1].msg_image_rect.centery = self.answers[-1].msg_image_rect.centery + 25
            self.second_lines_answers[-1].msg_image_rect.x = self.answers[-1].msg_image_rect.x

        eg_game.settings.question_button["font_size"] = 39


    def draw_question(self):
        """Отображение вопроса с вариантами ответов."""
        for que in self.questions:
            que.draw_button()
        for ans in self.answers:
            ans.draw_button()
        for ans in self.second_lines_answers:
            ans.draw_button()
