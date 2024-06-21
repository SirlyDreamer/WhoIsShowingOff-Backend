import random
import time

from utils import QuestionSet, UserDB

qset = QuestionSet()
users = UserDB()


class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, room_id):
        if room_id in self.rooms:
            return False
        self.rooms[room_id] = Room()
        return True

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def cleanup(self):
        for room_id in list(self.rooms.keys()):
            if len(self.rooms[room_id].players) == 0:
                self.rooms.pop(room_id)


class Room:
    def __init__(self):
        self.timeout = 5
        self.question_set = []
        self.players = set()
        self.scores = {}
        self.is_start = False

        self.question_index = 0
        self.question_show_time = 0
        self.correct_answer = None
        self.correct_index = -1

    def join(self, player: int):
        if self.is_start:
            return False
        self.players.add(player)
        self.scores[player] = users.get_user(player).score

    def leave(self, player: int):
        if player in self.players:
            users.update_user(player, {'score': self.scores[player]})
            self.scores.pop(player)
            self.players.remove(player)

    def start(self, num_questions=5):
        self.question_set = qset.pick_random_questions(num_questions)
        self.question_index = 0
        self.is_start = True

    def get_question(self):
        if self.question_index >= len(self.question_set):
            return None
        current_question = self.question_set[self.question_index]
        self.correct_answer = current_question['short_answer']
        options = [
            self.correct_answer,
            current_question['wrong_answer_1'],
            current_question['wrong_answer_2'],
            current_question['wrong_answer_3'],
            current_question['wrong_answer_4'],
            current_question['wrong_answer_5']
        ]
        random.shuffle(options)
        self.correct_index = options.index(self.correct_answer)
        self.question_show_time = time.time()
        return {'question': current_question['question'], 'options': options, 'reason': current_question['reason']}

    def next_question(self):
        # If nobody answers the question in time, the game will go to the next question
        self.question_index += 1
        return self.get_question()

    def check_answer(self, player: int, answer: int):
        # Check if the player's answer is correct
        if time.time() - self.question_show_time > self.timeout:
            return -1
        if answer == self.correct_index:
            self.scores[player] += 1
            self.question_index += 1
            return 1
        else:
            return 0

    def finalize(self):
        for player in self.players:
            users.update_user(player, {'score': self.scores[player]})
        self.is_start = False
