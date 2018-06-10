#from app import fb
import json
class Mirror:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.mirror_uid = self.recv_msg()['BODY']
        self.user_list = []
        self.user_uid = None
        #self.set_user_list()
        print('Connect to Pi Complete')

    def recv_msg(self):
        msg = self.client_socket.recv(4096)
        msg = msg.decode('utf-8')
        msg_dict = json.loads(msg)
        return msg_dict
    '''
    def set_user_list(self):
        from app import fb
        self.user_list = fb.get_user_list(self.mirror_uid)
        print(self.user_list)
    '''

    def send_msg(self, msg):
        msg = json.dumps(msg)
        msg = msg.encode('utf-8')
        self.client_socket.send(msg)
