import time
from flask import Flask, request
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://127.0.0.1:6379"
app.register_blueprint(sse, url_prefix='/events')


class Timer:
    def __init__(self, timeout, roomID):
        self.roomID = roomID
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
                sse.publish(data='timeout', type='timeout', channel=self.roomID)
                self.last_tick = time.time()
        self._stop = False
        self._reset = False

    def stop(self):
        self._stop = True

    def reset(self):
        self._reset = True


timers = {}


@app.post('/login')
def login():
    userID = "dummy_user"
    userName = "dummy_user_name"
    sse.publish(data={'userID': userID, 'userName': userName}, type='login')
    return {'status': 0, 'msg': 'Fake login signal sent'}


@app.post('/join')
def join():
    roomID = "dummy_room"
    userID = "dummy_user"
    sse.publish(data={'userID': userID, 'roomID': roomID}, type='join')
    return {'status': 0, 'msg': 'Fake join signal sent'}


@app.post('/leave')
def leave():
    roomID = "dummy_room"
    userID = "dummy_user"
    sse.publish(data={'userID': userID, 'roomID': roomID}, type='leave')
    return {'status': 0, 'msg': 'Fake leave signal sent'}


@app.post('/rooms/dummy_room/ready')
def ready(roomID):
    userID = "dummy_user"
    sse.publish(data={'userID': userID, 'roomID': "dummy_room"}, type='ready')
    return {'status': 0, 'msg': 'Fake ready signal sent'}


@app.post('/rooms/<roomID>/deready')
def deready(roomID):
    userID = "dummy_user"
    sse.publish(data={'userID': userID, 'roomID': "dummy_room"}, type='deready')
    return {'status': 0, 'msg': 'Fake deready signal sent'}


@app.post('/rooms/<roomID>/start')
def start(roomID):
    sse.publish(data={
        "total": 1,
        "players": ["dummy_player_1", "dummy_player_2", "dummy_player_3"],
        "scores": ["0", "0", "0"]
    }, type='start', channel="dummy_room")
    return {'status': 0, 'msg': 'Fake start signal sent'}


@app.get('/rooms/<roomID>/question')
def question(roomID):
    userID = "dummy_user"
    sse.publish(data={'userID': userID, 'roomID': "dummy_room", 'question': 'Fake question'}, type='question')
    return {'status': 0, 'msg': 'Fake question signal sent'}


@app.post('/rooms/<roomID>/submit')
def competition(roomID):
    userID = "dummy_user"
    answer = "dummy_answer"
    sse.publish(data={'userID': userID, 'roomID': "dummy_room", 'answer': answer}, type='answer')
    return {'status': 0, 'msg': 'Fake answer signal sent'}


if __name__ == '__main__':
    app.run(host='localhost', port=11451)