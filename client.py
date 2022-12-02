from socket import *
import utils


class Client:
    '''
    通过TCP连接获取服务器时钟并同步相关控件
    基于UDP直接交换聊天信息
    支持两种聊天模式 一对一 一对多
    '''
    def __init__(self,ip, port):
        self.ip = ip
        self.port = port


    def signin(self, username, password):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        send_data = utils.send_signin(username, password)
        print(type(send_data))
        self.client_socket.send(send_data.encode())
        back_str = self.client_socket.recv(1024).decode()
        back_data=eval(back_str)
        self.client_socket.close()
        return back_data['code']

    def updata(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        send_data = utils.send_updata()
        print(type(send_data))
        self.client_socket.send(send_data.encode())
        back_str = self.client_socket.recv(1024).decode()
        back_data = eval(back_str)
        print(back_data)
        self.client_socket.close()
        return back_str


if __name__ == '__main__':
    c1 =Client('127.0.0.1', 3434)
    c1.signin('root','password')
    c1.updata()