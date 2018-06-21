import socket
import threading
from app import Mirror


class pi_connector(threading.Thread):

    def __init__(self, host, port):
        self.mirror_list = {}#mirror_list
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
            self.mirror_list[mirror.mirror_uid] = mirror

    def authenticate(self, mirror_uid, head, body):
        str = 'False'
        try:
            send_dict = self.create_dict(head, body)
            self.mirror_list[mirror_uid].send_msg(send_dict)
            auth_dict = self.mirror_list[mirror_uid].recv_msg()
            print('PI Connector [')
            if auth_dict['BODY'] is True:
                str = 'True'
        except Exception as e:
            pass
        finally:
            return str

    def update_pi(self, mirror_uid, user_uid, head, body):
        str = 'False'
        try:
            if self.mirror_list[mirror_uid].user_uid == user_uid:
                send_dict = self.create_dict(head, body)
                self.mirror_list[mirror_uid].send_msg(send_dict)
                str = 'True'
        except Exception as e:
            pass
        finally:
            return str

    def create_dict(self, head, body):
        msg_dict = {
            'HEAD': head,
            'BODY': body,
        }
        return msg_dict

    def send_msg_to_all(self, msg):
        try:
            for key in self.mirror_list:
                self.mirror_list[key].send_msg(msg)
        except Exception as e:
            self.mirror_list.pop(key)
            print('pi_connector.py send_msg_to_all error')
        #msg = msg.encode('utf-8')
        #self.sock.send(msg)
