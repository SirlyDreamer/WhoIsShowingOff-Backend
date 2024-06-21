# flask API with SSE
from flask import Flask, Response, request
from utils import UserDB

app = Flask(__name__)

users = UserDB()
@app.post('/login')
def login():
    userID = request.json.get('userID')
    userName = request.json.get('userName', str(userID))
    if users.get_user(userID):
        return {'status': 0, 'msg': 'Login success'}
    else:
        users.add_user(userID, userName)
        return {'status': 0, 'msg': 'Register success'}

@app.get('/join')
def join():
    roomID = request.args.get('roomID')
