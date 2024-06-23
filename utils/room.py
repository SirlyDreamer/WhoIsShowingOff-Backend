import json
import random
import time

from utils import QuestionSet, UserDB

qset = QuestionSet()
users = UserDB()


class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create(self, room_id, user_id):
        self.rooms[room_id] = Room(user_id)
        return True

    def exists(self, room_id):
        return room_id in self.rooms

    def get(self, room_id):
        return self.rooms.get(room_id)

    def cleanup(self):
        for room_id in list(self.rooms.keys()):
            if len(self.rooms[room_id].players) == 0:
                self.rooms.pop(room_id)


class Room:
    def __init__(self, owner=None):
        self.timeout = 5
        self.question_set = []
        self.owner = owner
        self.players = {owner}
        self.ready_players = set()
        self.scores = {
            owner: users.get_user(owner).score
        }
        self.is_start = False
        self.event = None

        self.question_index = 0
        self.question = None
        self.question_show_time = 0
        self.answer = -1

    def set_owner(self, owner):
        # 转移房主
        self.owner = owner

    def join(self, player: str):
        # 加入房间
        if self.is_start:
            return False
        self.players.add(player)
        self.scores[player] = users.get_user(player).score
        return True

    def leave(self, player: str):
        # 离开房间（结算分数）
        # TODO: 游戏开始后能否离开房间
        if player in self.players:
            users.update_user(player, {'score': self.scores[player]})
            self.scores.pop(player)
            self.players.remove(player)

    def is_in_room(self, player):
        return player in self.players

    def is_owner(self, player):
        return player == self.owner

    def is_all_ready(self):
        return len(self.ready_players) == len(self.players)

    def start(self, num_questions=15):
        self.question_set = qset.pick_random_questions(num_questions)
        self.question_index = 0
        self.is_start = True

    def ready(self, player: int):
        self.ready_players.add(player)

    def deready(self, player: int):
        self.ready_players.remove(player)

    def status(self):
        return self.is_start, self.ready_players, self.players

    def get_question(self):
        if not self.is_start:
            return None
        if self.question_index >= len(self.question_set):
            return None
        return {
            'question': self.question['question'],
            'options': self.question['options'],
            'reason': self.question['reason']
        } if self.question is not None else None

    def next_question(self):
        # If nobody answers the question in time, the game will go to the next question
        self.question_index += 1
        self.question_show_time = time.time()
        if self.question_index >= len(self.question_set):
            self.finalize()
            self.question = None
            return None
        question_id = self.question_set[self.question_index]
        self.question = qset.get_question(question_id)
        self.answer = self.question['answer']
        print(json.dumps(self.question, ensure_ascii=False, indent=2))
        return self.question

    def check_answer(self, player: int, answer: int):
        # Check if the player's answer is correct
        if time.time() - self.question_show_time > self.timeout:
            return -1
        if answer == self.answer:
            self.scores[player] += 1
            self.next_question()
            return 1
        else:
            return 0

    def finalize(self):
        for player in self.players:
            users.update_user(player, {'score': self.scores[player]})
        self.is_start = False
        self.ready_players.clear()
