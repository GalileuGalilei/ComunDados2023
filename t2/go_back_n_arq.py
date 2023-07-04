import random
import time

class go_back_n_arq_client:

    def __init__(self, windows_size, max_frame_id):
        self.max_frame_id = max_frame_id
        self.windows_size = windows_size
        self.expected_frame = 0

    #executa toda vez que o client receber um pacote
    def receive_frame_ack(self, ack_id):
        #10% de chance de perder o pacote
        if ack_id == self.expected_frame and random.randint(0, 100) < 50:
            self.expected_frame += 1
            return True
        else:
            return False
    
class go_back_n_arq_server:
    #max_frame_id = 0
    #window_size = 0
    #current_last_frame = 0

    def __init__(self, window_size, max_frame_id, time_out):
        self.window_size = window_size
        self.available_frames = window_size + 1
        self.available_frames = window_size + 1
        self.max_frame_id = max_frame_id
        self.time_out = time_out
        self.current_last_frame = -1
        self.timer = 0
        self.last_timer_reset = time.time()

    #executa toda vez que o server receber um pacote
    def receive_frame_ack(self, ack_id):
        #verifica se é um id esperado
        if ack_id == 255:
            self.available_frames = self.window_size
            self.current_last_frame -= self.window_size
            if self.current_last_frame < 0:
                self.current_last_frame = 0
            return 0

        if(ack_id > self.current_last_frame or ack_id < self.current_last_frame - self.window_size):
            return 0
            
        diff = self.window_size - (self.current_last_frame - ack_id) + 1
        self.available_frames += diff
        self.last_timer_reset = time.time()

        return diff
    
    #executa toda santa iteração do loop
    def send_frame_ack(self):

        self.timer = time.time() - self.last_timer_reset
        if self.timer > self.time_out:
            print("Time out")
            self.last_timer_reset = time.time()
            self.available_frames = self.window_size
            self.current_last_frame -= self.window_size
            if self.current_last_frame < 0:
                self.current_last_frame = 0

        if self.available_frames == 0:
            return -1
        
        self.available_frames -= 1
        self.current_last_frame += 1
        return self.current_last_frame