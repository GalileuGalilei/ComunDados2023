class go_back_n_arq_client:

    def __init__(self, windows_size, max_frame_id):
        self.max_frame_id = max_frame_id
        self.windows_size = windows_size
        self.expected_frame = 0

    #executa toda vez que o client receber um pacote
    def receive_frame_ack(self, ack_id):
        if ack_id == self.expected_frame:
            self.expected_frame += 1
            if self.expected_frame > self.max_frame_id:
                self.expected_frame = 0
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
        self.max_frame_id = max_frame_id
        self.time_out = time_out
        self.current_last_frame = -1
        self.timer = 0

    #executa toda vez que o server receber um pacote
    def receive_frame_ack(self, ack_id):
        #verifica se é um id esperado
        if(self.current_last_frame < ack_id):
            #caso easy
            if(ack_id - self.current_last_frame > self.window_size):
                #print("VARIAVEL FORA DO RANGE DA JANELA ERRO")  
                return 0
        else:
            #caso chato
            if(ack_id > self.current_last_frame):
                #print("VARIAVEL FORA DO RANGE DA JANELA ERRO")  
                return 0
        

        if(self.current_last_frame <= ack_id):
            print('caso chato')
            diff = self.max_frame_id - ack_id + self.current_last_frame
        else:
            print('caso easy')
            diff = ack_id
        # mandou 0 1 2 3 4 
        # recebe 0 1
        # janela     2 3 4 5 6
        self.available_frames += diff + 1
        self.timer = 0

        return diff + 1
    
    #executa toda santa iteração do loop
    def send_frame_ack(self, delta_time):

        self.timer += delta_time
        if self.timer > self.time_out:
            print("Time out")
            self.timer = 0
            self.available_frames = self.window_size
            self.current_last_frame -= self.window_size
            if self.current_last_frame < 0:
                self.current_last_frame = self.max_frame_id + self.current_last_frame + 1

        if self.available_frames == 0:
            return -1
        
        self.available_frames -= 1
        self.current_last_frame += 1
        if self.current_last_frame > self.max_frame_id:
            self.current_last_frame = 0
        return self.current_last_frame