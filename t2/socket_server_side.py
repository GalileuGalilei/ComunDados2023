import socket
import math	
import go_back_n_arq	
import crc

#converte um int para uma lista de bits
def integer_to_bit_list(integer):
    bits = bin(integer)[2:].zfill(8)
    return list(bits)

#converte uma string para uma lista de bits
def string_to_bit_list(string):
    bit_list = []
    for char in string:
        byte = ord(char)  
        bits = bin(byte)[2:].zfill(8) 
        bit_list.extend(list(bits)) 
    return bit_list

#adiciona um 0 apos encontrar 011111, evitando sequencias iguais a flag 01111110
def data_bit_stuffing(data):
    for i in range(len(data) - 6):
        if data[i : i+6] == ['0', '1', '1', '1', '1', '1']:
            data.insert(i+6, '0')

def list_to_string(list):
    return ''.join(list)

#monta o frame
def make_frame(data, polynomial, num_of_frames, frame_id):
    #monta a flag
    flag = ['0', '1', '1', '1', '1', '1', '1', '0']

    #monta o header com o numero de frames e o id do frame (nao necessariamente nessa ordem)
    header = []
    header += integer_to_bit_list(frame_id)
    header += integer_to_bit_list(num_of_frames)

    #monta o trailer com o crc
    remainder = crc.CRC(list_to_string(data), polynomial)
    
    trailer = integer_to_bit_list(len(remainder))

    #monta uma lista temporaria com header data e trailer
    tmp = []
    tmp += header
    tmp += data
    tmp += list(remainder)
    tmp += trailer

    #faz bit stuffing da mensagem com header e trailer
    data_bit_stuffing(tmp)

    #monta o frame apos o bitstuffing
    bitarray = []
    bitarray += flag
    bitarray += tmp
    bitarray += flag

    return bitarray

#separa a string original em uma lista de substrings, que serao convertidas em frames posteriormente
def separate_data(data, num_of_frames):
    data_pieces = []
    for i in range(num_of_frames - 1):
        data_pieces.append(data[i*100: (i+1)*100])

    data_pieces.append(data[(num_of_frames-1)*100: ])
    return data_pieces

#retorna apenas a ultima mensagem de acknoledge enviada pelo cliente, caso alguns acks tenham sido concatenados
def separate_ack(ack):
    acks = ack.split("_")

    if(len(acks) < 2):
        return -1
     
    return acks[-2]

#inicializa o socket e cria a conexao
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
    data = "\nNo vasto cosmos, uma nave flutua,\nEntre tripulantes, segredos se insinuam.\nNo jogo de traicao, intriga e suspense,\nAmong Us revela-se, um verdadeiro cadence.\n\nNa sala de reunioes, mentes se confrontam,\nOlhares desconfiados, acusacoes que assombram.\nCada suspeito tem um alibi em seu favor,\nMas a verdade esconde-se alem do rumor.\n\nEntre corredores sombrios, em silencio caminham,\nProcurando pistas, enquanto a nave estremece e gira.\nUma tarefa inacabada, uma sabotagem fria,\nA busca pela verdade jamais se adia.\n\nAs votacoes decidem o destino de todos,\nLealdade e astucia, sao seus maiores modos.\nQuem e o impostor, o infiltrado traidoeiro?\nDesvendar esse enigma e o grande truque derradeiro.\n\nEntre o caos e a desconfianca, a camaradagem resiste,\nTripulantes unidos, buscando um final que persiste.\nNas reunioes emergem historias e aliancas,\nEntre acusacoes e jogadas, emocoes e esperancas.\n\nAmong Us, o jogo de suspense e decepcao,\nOnde a estrategia se entrelaca a diversao.\nEm cada partida, uma nova narrativa se desenha,\nOnde a vitoria e conquistada, mas a desconfianca permanece.\n\nPortanto, tripulantes, estejam preparados,\nPara enfrentar traidores, serem astutos e ousados.\nEm cada partida, um novo desafio emerge,\nEntre suspeitas e misterios, a verdade se converge.\n\nEntre amigos e desconhecidos, a jornada continua,\nAmong Us, o jogo que cativa e perpetua.\nDesvende os enigmas, encontre o impostor,\nE mergulhe neste universo de traicao e temor."
    data = string_to_bit_list(data)

    #separa o dado a ser enviado em diferentes pedacos, que serao transformados em frames
    num_of_frames = int(math.ceil(len(data)/100))
    data_pieces = separate_data(data, num_of_frames)
    #polinomio para crc-8
    polynomial = '100000111'


    s = create_connection()

    c, addr = s.accept()
    c.settimeout(1) #define o tempo para envios e recebimentos resultarem em timeout

    go_back = go_back_n_arq.go_back_n_arq_server(4, 12)
    print ('Got connection from', addr)

    i = 0
    ack = '-1' #valor impossivel   

    while True:            

        #se recebeu algum acknoledge, calcula o proximo valor de inicio da janela
        if(ack != '-1'):
            i = go_back.receive_frame_ack(ack, i)

        #retorna qual o proximo frame a ser enviado, caso exista algum frame nao enviada na janela
        frame_id = go_back.send_frame_ack()

        #se todos os frames foram enviados, espera resposta do client
        if(frame_id == -1):
            try:   
                ack = c.recv(1024).decode()
                ack = separate_ack(ack)
                print("recieved ack " + ack)
            except socket.timeout: #caso nao receba a resposta, chama a funcao trigger_timeout, que volta a janela
                print('timeout recieve')
                go_back.trigger_timeout()
                ack = '-1'
            continue

        #se todos os frames ja foram mandados
        if(frame_id >= num_of_frames):
            try:
                ack = c.recv(2048).decode()
                ack = separate_ack(ack)
                print("recieved ack " + ack)
                if ack == '-2': #se o client enviou -2, significa que ele processou todos os frames
                    print('client disconnected')
                    c.close()
                    break
            except socket.timeout:
                print("timeout recieve")
        else: #se ainda tem frames para mandar, manda
            try:
                print("sent frame ", frame_id)
                frame = make_frame(data_pieces[frame_id], polynomial, num_of_frames, frame_id)
                c.sendall(list_to_string(frame).encode())
            except socket.timeout:
                print("send timeout")

if __name__ == '__main__':
    main()