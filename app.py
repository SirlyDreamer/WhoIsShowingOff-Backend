# flask API with SSE
import time

from flask import Flask, request
from flask_sse import sse

from utils import UserDB, RoomManager

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://127.0.0.1:6379"
app.register_blueprint(sse, url_prefix='/events')

users = UserDB()
users.create_table()

rooms = RoomManager()


class Timer:
    def __init__(self, timeout, roomID):
        self.roomID = roomID
        self.room = rooms.get(roomID)
        self.timeout = timeout
        self.last_tick = time.time()
        self._stop = False
        self._reset = False

    def start(self):
        self._stop = False
        self.last_tick = time.time()
        while not self._stop:
            if self._reset:
                self.last_tick = time.time()
                self._reset = False
            if time.time() - self.last_tick >= self.timeout:
                self.room.next_question()
                sse.publish('timeout', type='timeout', channel=self.roomID)
                self.last_tick = time.time()
        self._stop = False
        self._reset = False

    def stop(self):
        self._stop = True

    def reset(self):
        self._reset = True


timers = {}


# 需求：1. 提供登录注册接口，该接口仅用于向数据库中写入用户（注册），不进行验证，登陆或注册成功后则返回信息
@app.post('/login')
def login():
    userID = str(request.json.get('userID'))
    userName = str(request.json.get('userName', str(userID)))
    if users.get_user(userID):
        return {'status': 0, 'msg': 'Login success'}
    else:
        users.add_user(userID, userName)
        return {'status': 0, 'msg': 'Register success'}


# 需求：2. 提供加入/创建房间接口，该接口用于加入/创建房间，返回房间ID
@app.post('/join')
def join():
    # TODO: 返回房间信息
    roomID = str(request.json.get('roomID', '0000'))
    userID = str(request.json.get('userID'))
    if rooms.exists(roomID):
        room = rooms.get(roomID)
        if room.join(userID):
            sse.publish(data=userID, type='join', channel=roomID)
            return {'status': 0, 'msg': '加入成功！'}
        else:
            return {'status': -1, 'msg': '该房间游戏已经开始了！'}
    else:
        rooms.create(roomID, userID)
        return {'status': 0, 'msg': '创建房间成功！'}


@app.post('/leave')
def leave():
    roomID = str(request.json.get('roomID', '0000'))
    userID = str(request.json.get('userID'))
    if rooms.exists(roomID):
        room = rooms.get(roomID)
        room.leave(userID)
        sse.publish(data=userID, type='leave', channel=roomID)
        return {'status': 0, 'msg': '离开成功！'}
    else:
        return {'status': -1, 'msg': '房间不存在！'}


# 之后的API为对房间的操作


@app.post('/rooms/<roomID>/ready')
def ready(roomID):
    roomID = str(request.view_args['roomID'])
    if not rooms.exists(roomID):
        return {'status': -1, 'msg': '房间不存在！'}, 404
    userID = str(request.json.get('userID'))
    room = rooms.get(roomID)
    room.ready(userID)
    sse.publish(data=userID, type='ready', channel=roomID)
    return {'status': 0, 'msg': '准备成功！'}


@app.post('/rooms/<roomID>/deready')
def deready(roomID):
    roomID = str(request.view_args['roomID'])
    if not rooms.exists(roomID):
        return {'status': -1, 'msg': '房间不存在！'}, 404
    userID = str(request.json.get('userID'))
    room = rooms.get(roomID)
    room.deready(userID)
    sse.publish(data=userID, type='deready', channel=roomID)
    return {'status': 0, 'msg': '取消准备成功！'}


@app.post('/rooms/<roomID>/start')
def start(roomID):
    roomID = str(request.view_args['roomID'])
    if not rooms.exists(roomID):
        return {'status': -1, 'msg': '房间不存在！'}, 404
    userID = str(request.json.get('userID'))
    room = rooms.get(roomID)
    if not room.is_owner(userID):
        return {'status': -2, 'msg': '只有房主可以开始游戏！'}, 403
    if not room.is_all_ready():
        return {'status': -3, 'msg': '还有玩家未准备！'}
    timers[roomID] = Timer(5, roomID)
    sse.publish(data={
        "total": len(room.question_set),
        "players": list(room.players),
        "scores": list(room.scores)
    }, type='start', channel=roomID)
    timers[roomID].start()
    room.start()
    return {'status': 0, 'msg': '游戏开始！'}


@app.get('/rooms/<roomID>/question')
def question(roomID):
    # 当客户端接收到'start', 'answer', 'timeout'事件后，调用此接口获取题目
    roomID = str(request.view_args['roomID'])
    if not rooms.exists(roomID):
        return {'status': -1, 'msg': '房间不存在！'}, 404
    room = rooms.get(roomID)
    if not room.is_start:
        return {'status': -2, 'msg': '比赛还未开始！'}, 403
    userID = request.args.get('userID')
    if userID not in room.players:
        return {'status': -3, 'msg': '您不在房间内！'}, 403
    return room.get_question(userID)


@app.post('/rooms/<roomID>/submit')
def competition(roomID):
    # SSE长连接，用于通知用户比赛状态
    # 事件：join, leave, ready, deready, start, answer, question, finish
    roomID = str(request.view_args['roomID'])
    if not rooms.exists(roomID):
        return {'status': -1, 'msg': '房间不存在！'}, 404
    room = rooms.get(roomID)
    if not room.is_start:
        return {'status': -2, 'msg': '比赛还未开始！'}, 403
    userID = str(request.json.get('userID'))
    if userID not in room.players:
        return {'status': -3, 'msg': '您不在房间内！'}, 403
    answer = request.json.get('answer')
    if room.check_answer(userID, answer):
        sse.publish(data=userID, type='answer', channel=roomID)
        room.next_question()
        timers[roomID].reset()
        return {'status': 0, 'msg': '回答正确！'}
