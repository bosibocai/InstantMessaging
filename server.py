import socket
import threading

import utils
import logging
import json
import time


logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            filename='usersInfo.log',
                            filemode='a')
class Server:
    '''
    维护用户账号和日志文件
    验证用户登录信息
    显示在线用户列表（用户名与IP地址）
    '''
    def __init__(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        tcp_socket.bind(('127.0.0.1', 3434))
        tcp_socket.listen(128)
        self.tcp_server_socket = tcp_socket
        self.onlineUsers = {}
        self.users = self.loadUsers()
        self.nums = 0

    def loadUsers(self):
        with open('users.json','r',encoding='utf-8')as f:
            json_data = json.load(f)
            return json_data

    def signin(self, content):
        u = content['username']
        p = content['password']
        password = self.users.get(u)
        if password==None:
            logging.info("sign in fail: username error!")
            return False, ""
        else:
            if password == p:
                # 登录成功
                logging.info("sign in success!")
                return True, u
            else:
                logging.info("sign in fail: password error!")
                return False, ""

    def updata(self):
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(time_str)
        return utils.response_updata(time_str, self.onlineUsers)



    def service(self, tcp_client, tcp_client_address,tcp_client_id):
        while True:
            recv_data = tcp_client.recv(1024)
            if recv_data:
                recv = eval(recv_data.decode())
                comment = recv['comment']
                if comment == 'signin':
                    code, user = self.signin(recv['content'])
                    tcp_client.send(utils.response_signin(str(code)).encode())
                    if code:
                        # self.onlineUsers[user] = (tcp_client, tcp_client_address)
                        self.onlineUsers[user] = tcp_client_address
                if comment == 'updata':
                    tcp_client.send(self.updata().encode())


        tcp_client.close()
        self.onlineUsers.pop(user)


    def start(self):
        print("python server start")
        while True:
            new_socket, client_addr = self.tcp_server_socket.accept()
            print("python client start")
            print("new client connect", client_addr)
            # 创建多线程对象
            thd = threading.Thread(target=self.service, args=(new_socket, client_addr, self.nums))
            self.nums += 1
            # 启动子线程对象
            thd.setDaemon(True)
            thd.start()
        print("python server start")

if __name__ == '__main__':
    s = Server()
    s.start()
