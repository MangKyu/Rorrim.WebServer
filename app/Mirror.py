from app import fb
class Mirror():
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.mirror_uid = self.client_socket.recv(4096).decode('utf-8')
        self.user_list = []
        self.set_user_list()
        print('Connect to Pi Complete')

    def set_user_list(self):
        self.user_list = fb.get_user_list(self.mirror_uid)
        print(self.user_list)

    def send_msg(self, msg):
        msg = msg.encode('utf-8')
        self.client_socket.send(msg)