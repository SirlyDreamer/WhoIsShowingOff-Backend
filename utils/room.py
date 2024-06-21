import random
from utils import QuestionSet, UserDB

qset = QuestionSet()
users = UserDB()
class RoomManager:
    def __init__(self):
        self.rooms = {}
class Room:
    def __init__(self, level=1):
        self.current_question = 0
        self.current_correct_answer = None
        self.current_correct_index = -1
        self.question_set = qset.pick_random_questions(level)
        self.players = set()
        self.scores = {}
        self.is_start = False

    def join(self, player: int):
        if self.is_start:
            return False
        self.players.add(player)
        self.scores[player] = users.get_user(player).score

    def leave(self, player: int):
        if player in self.players:
            self.players.remove(player)
            users.update_user(player, {'score': self.scores[player]})
            self.scores.pop(player)

    def start(self):
        self.is_start = True

    def get_question(self):
        current_question = self.question_set[self.current_question]
        self.current_correct_answer = current_question['short_answer']
        options = [
            self.current_correct_answer,
            current_question['wrong_answer_1'],
            current_question['wrong_answer_2'],
            current_question['wrong_answer_3'],
            current_question['wrong_answer_4'],
            current_question['wrong_answer_5']
        ]
        random.shuffle(options)
        self.current_correct_index = options.index(self.current_correct_answer)
        return {'question': current_question['question'], 'options': options, 'reason': current_question['reason']}

    def check_answer(self, player: int, answer: int):
        if answer == self.current_correct_index:
            self.scores[player] += 1
            return True
        else:
            return False