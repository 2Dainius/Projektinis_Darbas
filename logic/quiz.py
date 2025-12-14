import random
import re
from data.loader import load_questions

TOTAL_QUESTIONS = 12

class Quiz:
    def __init__(self):
        all_questions = load_questions()
        if len(all_questions) < TOTAL_QUESTIONS:
            raise ValueError(f"Nepakanka klausimų faile!")
        self.questions = random.sample(all_questions, TOTAL_QUESTIONS)

        self.current_index = 0
        self.user_answers = [None] * TOTAL_QUESTIONS
        self.finished = False

    def get_current_question(self):
        return self.questions[self.current_index]

    def answer(self, chosen_index: int):
        self.user_answers[self.current_index] = chosen_index

    def next(self):
        if self.current_index < TOTAL_QUESTIONS - 1:
            self.current_index += 1
        else:
            self.finished = True

    def previous(self):
        if self.current_index > 0:
            self.current_index -= 1

    def calculate_score(self):
        score = 0
        for i, q in enumerate(self.questions):
            if self.user_answers[i] == q["correct"]:
                score += 1
        return score

    def is_finished(self):
        return self.finished

