import json
import time

from utils import QuestionSet, UserDB

qset = QuestionSet()
users = UserDB()


class RoomManager:
    def __init__(self):
        self.rooms = {}
        self.create('0000', 'admin')

    def create(self, room_id, user_id):
        self.rooms[str(room_id)] = Room(user_id)
        return True

    def exists(self, room_id):
        return str(room_id) in self.rooms

    def get(self, room_id):
        return self.rooms.get(str(room_id))

    def cleanup(self):
        for room_id in list(self.rooms.keys()):
            if len(self.rooms[room_id].players) == 0:
                self.rooms.pop(room_id)


class Room:
    def __init__(self, owner=None, timeout=5):
        self.timeout = timeout
        self.question_set = []
        owner_info = users.get_user(owner)
        self.owner = (owner_info.userID, owner_info.userName)
        self.players = set()
        self.players.add((owner_info.userID, owner_info.userName))
        self.ready_players = set()
        self.scores = {
            owner_info.userID: 0
        }
        self.is_start = False
        self.allow_submit = False
        self.event = None

        self.question_index = 0
        self.question = None
        self.answer = -1

    def set_owner(self, owner):
        # 转移房主
        self.owner = owner

    def join(self, player: str):
        # 加入房间
        if self.is_start:
            return False
        player_info = users.get_user(player)
        self.players.add((player_info.userID, player_info.userName))
        # self.scores[player] = player_info.score
        self.scores[player_info.userID] = 0
        return True

    def leave(self, player: str):
        # 离开房间（结算分数）
        # TODO: 游戏开始后能否离开房间
        if player in self.players:
            player_info = users.get_user(player)
            # users.update_user(player, {'score': self.scores[player_info.userID]})
            self.scores.pop(player_info.userID)
            self.players.remove((player_info.userID, player_info.userName))

    def is_in_room(self, player):
        player_info = users.get_user(player)
        return (player_info.userID, player_info.userName) in self.players

    def is_owner(self, player):
        return player == self.owner[0]

    def is_all_ready(self):
        return len(self.ready_players) == len(self.players)

    def start(self, num_questions=15):
        self.question_set = qset.pick_random_questions(num_questions)
        self.question_index = 0
        self.is_start = True

    def ready(self, player: str):
        self.ready_players.add(player)

    def deready(self, player: str):
        self.ready_players.remove(player)

    def scoreboard(self):
        scores = []
        for player in self.players:
            scores.append({
                'userID': player[0],
                'userName': player[1],
                'score': self.scores[player[0]],
            })
        return scores

    def get_question(self):
        if not self.is_start:
            return None
        if self.question_index >= len(self.question_set):
            return None
        return {
            'question': self.question['question'],
            'options': self.question['options'],
            'time': self.timeout,
        } if self.question is not None else None

    def get_answer(self):
        if self.allow_submit:
            return None
        return {
            'answer': self.answer,
            'reason': self.question['reason'],
        }

    def get_players(self):
        return self.players

    def next_question(self):
        # If nobody answers the question in time, the game will go to the next question
        self.question_index += 1
        if self.question_index >= len(self.question_set):
            self.finalize()
            self.question = None
            return None
        question_id = self.question_set[self.question_index]
        self.question = qset.get_question(question_id)
        self.answer = self.question['answer']
        print(json.dumps(self.question, ensure_ascii=False, indent=2))
        self.allow_submit = True
        return self.question

    def check_answer(self, player: str, answer: int):
        # Check if the player's answer is correct
        if not self.allow_submit:
            return -1
        if answer == self.answer:
            self.scores[str(player)] += 1
            # self.next_question()
            return 1
        else:
            return 0

    def finalize(self):
        # for player in self.players:
        #     users.update_user(player, {'score': self.scores[player]})
        self.is_start = False
        self.allow_submit = False
        self.ready_players.clear()
