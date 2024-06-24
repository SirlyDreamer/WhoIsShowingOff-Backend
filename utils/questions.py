import json
import random


class QuestionSet:
    def __init__(self):
        self.questions = {}
        with open('data/questions.jsonl', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                current_question = json.loads(line)
                current_id = current_question['id']
                correct_answer = current_question['short_answer']
                options = [
                    correct_answer,
                    current_question['wrong_answer_1'],
                    current_question['wrong_answer_2'],
                    current_question['wrong_answer_3'],
                    current_question['wrong_answer_4'],
                    current_question['wrong_answer_5']
                ]
                random.shuffle(options)
                correct_index = options.index(correct_answer)
                question = {
                    'id': current_id,
                    'question': current_question['question'],
                    'options': options,
                    'answer': correct_index,
                    'reason': current_question['reason']
                }
                self.questions[current_id] = question
        self.indexes = list(self.questions.keys())

    def pick_random_questions(self, k: int = 1):
        return random.sample(self.indexes, k)

    def get_question(self, question_id):
        return self.questions.get(question_id)


