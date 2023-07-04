import socket
import math	
import go_back_n_arq	
import time

#converte um int para uma lista de bits
def integer_to_bit_list(integer):
    bits = bin(integer)[2:].zfill(8)  # Convert the ASCII value to a binary string
    return list(bits)

#converte uma string para uma lista de bits
def string_to_bit_list(string):
    bit_list = []
    for char in string:
        byte = ord(char)  # Get the ASCII value of the character
        bits = bin(byte)[2:].zfill(8)  # Convert the ASCII value to a binary string
        bit_list.extend(list(bits))  # Add each bit to the bit list
    return bit_list

#frame 
#flag = 01111110
def data_bit_stuffing(data):
    for i in range(len(data) - 6):
        if data[i : i+6] == ['0', '1', '1', '1', '1', '1']:
            data.insert(i+6, '0')

def list_to_string(list):
    return ''.join(list)

#monta o frame
def make_frame(data, num_of_frames, frame_id):
    #monta a flag
    flag = ['0', '1', '1', '1', '1', '1', '1', '0']

    #monta o header com o numero de frames e o id do frame (nao necessariamente nessa ordem)
    header = []
    header += integer_to_bit_list(frame_id)
    header += integer_to_bit_list(num_of_frames)

    #faz bit stuffing da mensagem
    data_bit_stuffing(data)

    #monta o trailer, por enquanto, 8 '0's
    trailer = ['0'] * 8

    #monta o frame
    bitarray = []
    bitarray += flag
    bitarray += header
    bitarray += data
    bitarray += trailer
    bitarray += flag

    return bitarray

def separate_data(data, num_of_frames):
    data_pieces = []
    for i in range(num_of_frames - 1):
        data_pieces.append(data[i*100: (i+1)*100])

    data_pieces.append(data[(num_of_frames-1)*100: ])

    return data_pieces

def create_connection():
    s = socket.socket()		
    print ("Socket successfully created")
    port = 12345			

    s.bind(('', port))		
    print ("socket binded to %s" %(port))

    s.listen(5)	
    print ("socket is listening")

    return s

def main():

    # define a mensagem a ser enviada e transforma em uma lista de bits
    data = 'Chupa meu pau Amogus SUS hahaha memes cu sexo ola pessoal yee aeee caralhooooow fe da putAAAAAAAAAAAAAAAAAAA ps. Manda nudes fds'
    data = string_to_bit_list(data)

    #separa o dado a ser enviado em diferentes pedacos, que serao transformados em frames
    num_of_frames = math.ceil(len(data)/100)
    data_pieces = separate_data(data, num_of_frames)


    i = 0
    s = create_connection()
    c, addr = s.accept()
    go_back = go_back_n_arq.go_back_n_arq_server(4, 12, 1)
    print ('Got connection from', addr)
    first = True
    ack = b'XX' #valor impossível   

    while True:            

        if first:
            print("client connected")
            
            first = False
        else:
            print('ack eh', int.from_bytes(ack, "big"))
            i += go_back.receive_frame_ack(int.from_bytes(ack, "big"))
            ack = b''
            print("novo i = ", i)

        frame_id = go_back.send_frame_ack()

        if(frame_id == -1):
            ack = c.recv(2048)
            continue

        if(frame_id >= num_of_frames):
            ack = c.recv(1024)
            if ack == b'':
                print('client disconnected')
                c.close()
                break
        else:
            c.sendall(list_to_string(make_frame(data_pieces[frame_id], num_of_frames, frame_id)).encode())


if __name__ == '__main__':
    main()