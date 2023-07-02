# Import socket module
import socket                    
 
def get_data_from_frame(frame):
    #monta a flag referencia
    flag = ['0', '1', '1', '1', '1', '1', '1', '0']

    #pega o header, corpo da msg, trailer e flag da msg
    header = frame[8:16]
    data = frame[16:-16]
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

    #retorna a mensagem
    size = int(''.join(header), 2)
    return data[:size]

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
    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect            
    port = 12345   
    # connect to the server on local computer
    s.connect(('127.0.0.1', port))

    # receive data from the server and decoding to get the string.
    raw_data = s.recv(1024)
    data = get_data_from_frame(list(raw_data.decode()))
    #remove o bit extra do bit stuffing
    remove_bit_stuffing(data)
    
    #printa a mensagem decodificada
    print(bit_list_to_string(data))
    # close the connection
    s.close() 

if __name__ == '__main__':
    main()