import json
import random


class QuestionSet:
    def __init__(self):
        self.questions = []
        with open('data/questions.jsonl', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                question = json.loads(line)
                self.questions.append(question)


    def pick_random_questions(self, k: int = 1):
        return random.sample(self.questions, k)

