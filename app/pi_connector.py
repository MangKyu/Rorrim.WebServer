import socket
import threading
from app import Mirror


class pi_connector(threading.Thread):

    def __init__(self, host, port):
        self.mirror_list = []#mirror_list
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.wait_for_client(host, port)
        threading.Thread.__init__(self)

    def wait_for_client(self, host, port):
        self.server_socket.bind((host, port))
        self.server_socket.listen(10)

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            mirror = Mirror.Mirror(client_socket)
            self.mirror_list.append(mirror)

    def create_dict(self, head, body):
        msg_dict ={
            'HEAD': head,
            'BODY': body,
        }
        return msg_dict

    def send_msg_to_all(self, msg):
        try:
            for i in range(len(self.mirror_list)):
                self.mirror_list[i].send_msg(msg)
        except Exception as e:
            print('pi_connector.py send_msg_to_all error')
        #msg = msg.encode('utf-8')
        #self.sock.send(msg)
