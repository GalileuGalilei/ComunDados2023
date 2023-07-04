# Import socket module
import socket                  
import go_back_n_arq  

def get_rest(trailer):
    for i in range(trailer.len()):
        if trailer[i] != 0:
            return i
        
def check_crc(data):
    dvd = int(''.join(data[:]), 2)
    dvs = int(''.join([1, 1, 0, 1]), 2)
    return (dvd % dvs) == 0
 
def get_data_from_frame(frame):
    #monta a flag referencia
    flag = ['0', '1', '1', '1', '1', '1', '1', '0']

    #pega o header, corpo da msg, trailer e flag da msg
    header = frame[8:24]
    data = frame[24:-16]
    trailer = frame[-16:-8]
    flag2 = frame[-8:]

    #compara as flags
    if flag != flag2:
        print("Error: flag != flag2")
        return None

    frame_id = int(''.join(header[:8]), 2)
    num_of_frames = int(''.join(header[8:]), 2)

    #retorna a mensagem
    return data, frame_id, num_of_frames

def separate_data_in_frames(raw_data):
    start = 0
    end = 0
    frames = []
    frame = []
    flag =  ['0', '1', '1', '1', '1', '1', '1', '0'] 
    
    flag_count = 0
    for i in range(len(raw_data) - 7):
        if(raw_data[i:i+8] == flag):
            flag_count += 1

            if(flag_count == 1):
                frame_start = i
            
            if(flag_count == 2):
                frame_end = i+8

                frame = raw_data[frame_start:frame_end] 
                frames.append(frame)
                # i = frame_end 
                flag_count = 0

    return frames

#converte lista de bits pra string
def bit_list_to_string(bit_list):
    byte_list = ["".join(bit_list[i:i+8]) for i in range(0, len(bit_list), 8)]  # Group bits into bytes
    char_list = [chr(int(byte, 2)) for byte in byte_list]  # Convert bytes to characters
    return "".join(char_list)

#remove o bit stuffing
def remove_bit_stuffing(data):
    for i in range(len(data) - 7):
        if data[i : i+7] == ['0', '1', '1', '1', '1', '1', '0']:
            data.pop(i+6)

def main():
    # Cria um socket, associa a porta 12345 e conecta ao servidor local
    s = socket.socket()
    port = 12345   
    s.connect(('127.0.0.1', port))

    #string final para concatenar os dados dos frames
    final_data = []

    #primeira mensagem
    go_back = go_back_n_arq.go_back_n_arq_client(4, 12)
    s.send(b'')

    while True:

        raw_data = s.recv(2048)
        if not raw_data:
            print('recebeu vazio')
            break
    
        frames = separate_data_in_frames(list(raw_data.decode()))
        last_frame_id = -1
        
        for frame in frames:
            data, frame_id, num_of_frames = get_data_from_frame(frame)
            
            #verifica se o frame é valido
            print("frame = %d" %(frame_id) )
            if go_back.receive_frame_ack(frame_id):

                print("Frame valido")

                remove_bit_stuffing(data)
                final_data += data
                last_frame_id = frame_id

            else:
                print("Frame invalido")
                s.send(bytes([255]))
                
        if last_frame_id != -1:
            print("enviado ack = ", last_frame_id)
            s.send(bytes([last_frame_id]))

        if(last_frame_id >= num_of_frames-1):
            s.send(b'')
            print("Fim da transmissao")
            break

    s.close() 
    messsage = bit_list_to_string(final_data)
    print(messsage)

if __name__ == '__main__':
    main()