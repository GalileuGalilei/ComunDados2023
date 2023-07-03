# Import socket module
import socket                    
 
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
    
    #verifica o trailer
    if trailer != ['0'] * 8:
        print("Error: trailer != ['0'] * 8")
        return None
    
    frame_id = int(''.join(header[:8]), 2)
    num_of_frames = int(''.join(header[8:]), 2)

    #retorna a mensagem
    return data, frame_id, num_of_frames

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
    while True:
        raw_data = s.recv(2048)
        print(raw_data)
        data, frame_id, num_of_frames = get_data_from_frame(list(raw_data.decode()))
        remove_bit_stuffing(data)

        final_data += data

        if(frame_id >= num_of_frames-1):
            s.close() 
            break
        #s.sendall(raw_data)
        
    messsage = bit_list_to_string(final_data)
    print(messsage)

if __name__ == '__main__':
    main()