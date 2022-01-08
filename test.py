import json
from random import choice


with open("questions.json", "r") as read_file:
    remaining_questions = json.load(read_file)

print(remaining_questions)


def get_msg():
    """Получаем рандомный вопрос из списка."""
    question = choice(list(remaining_questions))
    answers = remaining_questions[question]
    del remaining_questions[question]


get_msg()
print(remaining_questions)
