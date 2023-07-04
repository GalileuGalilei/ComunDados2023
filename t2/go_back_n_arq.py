import random

class go_back_n_arq_client:

    def __init__(self, windows_size, max_frame_id):
        self.max_frame_id = max_frame_id
        self.windows_size = windows_size
        self.expected_frame = 0

    #executa toda vez que o client receber um pacote
    def receive_frame_ack(self, ack_id):
        #10% de chance de perder o pacote
        if ack_id == self.expected_frame and random.randint(0, 100) < 90:
            self.expected_frame += 1
            return True
        else:
            return False
    
class go_back_n_arq_server:
    #max_frame_id = 0
    #window_size = 0
    #current_last_frame = 0

    def __init__(self, window_size, max_frame_id):
        self.window_size = window_size
        self.available_frames = window_size
        self.max_frame_id = max_frame_id
        self.current_last_frame = -1

    #executa toda vez que o server receber um pacote
    def receive_frame_ack(self, ack_id, i):
        #verifica se eh um id esperado
        ack_id = int(ack_id)

        if(ack_id > self.current_last_frame or ack_id <= self.current_last_frame - self.window_size):
            return i

        last_i = i
        i = ack_id + 1
        diff = i - last_i


        #diff = (self.current_last_frame - ack_id) + 1 - self.window_size
        self.available_frames += diff
        return i
    
    #executa toda santa iteracao do loop
    def send_frame_ack(self):

        if self.available_frames == 0:
            return -1
        
        self.available_frames -= 1
        self.current_last_frame += 1
        return self.current_last_frame
    
    def trigger_timeout(self):
        self.available_frames = self.window_size
        self.current_last_frame -= self.window_size
        if self.current_last_frame < 0:
            self.current_last_frame = -1