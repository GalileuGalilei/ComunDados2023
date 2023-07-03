class go_back_n_arq_client:
    current_windows_size = 0
    current_last_frame = 0


    def __init__(self, windows_size):
        self.windows_size = windows_size
    
class go_back_n_arq_server:
    current_windows_size = 0
    current_last_frame = 0
    window = []

    def __init__(self, windows_size):
        self.window = [False] * windows_size

    #retorna o if do frame esperado
    def send_frame(self):
        if(self.current_windows_size == len(self.window) - 1):
            return -1

        for i in range(len(self.window)):
            if self.window[i] == False:
                current_last_frame = i
                current_windows_size += 1
                return i
        return -1
    
    #retorna o if do frame esperado
    def receive_frame(self, frame_id):
        if frame_id >= len(self.window):
            return -1
        self.window[frame_id] = True
        self.current_windows_size -= 1
        return frame_id



