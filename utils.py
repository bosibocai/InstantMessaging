import json


def send_signin(username, password):
    dict = {
        'comment': 'signin',
        'content': {
            'username': username,
            'password': password
        }
    }
    return json.dumps(dict)


def response_signin(code):
    dict = {
        'code': code
    }
    return json.dumps(dict)

def send_updata():
    dict = {
        'comment': 'updata',
    }
    return json.dumps(dict)

def response_updata(time, onlineUsers):
    dict = {
        'time': time,
        'onlineUsers': onlineUsers
    }
    return json.dumps(dict)

