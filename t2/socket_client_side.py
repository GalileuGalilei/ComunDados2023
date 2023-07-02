#faça um socket server side
#faça um socket client side
#faça um socket server side que receba uma mensagem e retorne a mesma mensagem em maiúsculo
#faça um socket client side que envie uma mensagem e receba a mesma mensagem em maiúsculo

# Import socket module
import socket            
 
# Create a socket object
s = socket.socket()        
 
# Define the port on which you want to connect            

def get_data_from_frame(frame):
    flag = ['0', '1', '1', '1', '1', '1', '1', '0']
    header = frame[8:16]
    data = frame[16:-16]
    trailer = frame[-16:-8]
    flag2 = frame[-8:]

    if flag != flag2:
        print("Error: flag != flag2")
        return None

    if trailer != ['0'] * 8:
        print("Error: trailer != ['0'] * 8")
        return None

    size = int(''.join(header), 2)
    return data[:size]

def bit_list_to_string(bit_list):
    byte_list = ["".join(bit_list[i:i+8]) for i in range(0, len(bit_list), 8)]  # Group bits into bytes
    char_list = [chr(int(byte, 2)) for byte in byte_list]  # Convert bytes to characters
    return "".join(char_list)

def remove_bit_stuffing(data):
    for i in range(len(data) - 7):
        if data[i : i+7] == ['0', '1', '1', '1', '1', '1', '0']:
            data.pop(i+6)

# connect to the server on local computer
port = 12345   
s.connect(('127.0.0.1', port))


# receive data from the server and decoding to get the string.
raw_data = s.recv(10024)
data = get_data_from_frame(list(raw_data.decode()))
remove_bit_stuffing(data)
print(data)
print(bit_list_to_string(data))
# close the connection
s.close() 

