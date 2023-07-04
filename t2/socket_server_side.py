import socket
import math	
import go_back_n_arq	

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
def make_frame(data, num_of_frames, frame_id):
    #monta a flag
    flag = ['0', '1', '1', '1', '1', '1', '1', '0']

    #monta o header com o numero de frames e o id do frame (nao necessariamente nessa ordem)
    header = []
    header += integer_to_bit_list(frame_id)
    header += integer_to_bit_list(num_of_frames)

    #monta o trailer, por enquanto, 8 '0's
    trailer = ['0'] * 8

    #monta uma lista temporaria com header data e trailer
    tmp = []
    tmp += header
    tmp += data
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
    print(acks)

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
    #data = "No silencio espacial, tracoeiro eh o embuste, Um impostor oculto, um ser que seduz. Entre a tripulacao, um rosto oculto, No jogo de confianca, o Impostor eh astuto. Nas sombras ele se esconde, sorrateiro, Disfarcado de um amigo verdadeiro. Com olhos ardilosos, traca seu caminho, Espalhando enganos, semeando o desalinho. Passo a passo, ele tece sua rede, Manipula a mente, semeia a descrenca. Uma mascara perfeita, uma identidade falsa, Enredado nas mentiras, ele avanca. Em meio as tarefas e comunicacao, O Impostor provoca desconfianca e tensao. Cada suspeita, cada olhar desconfiado, Ele joga seu jogo, mantendo-se mascarado. Os corpos se acumulam, as acusacoes surgem, O Impostor ri, enquanto o caos se insurge. Mas o tempo eh seu inimigo, a pressa o consome, A tripulacao unida, determinada a encontrar o que se esconde. Por fim, a mascara cai, a verdade e revelada, O Impostor eh desmascarado, a farsa dissipada. Entre vidas perdidas e traicoes sofridas, A tripulacao vence, a vitoria eh conquistada. No jogo de Among Us, o Impostor eh a incognita, Um desafio ardiloso, uma historia infinita. Um poema se tece sobre esse ser ardente, Um impostor no jogo, eternamente surpreendente."
    data = "Ai! No alto daquele cume Plantei uma roseira O vento no cume bate A rosa no cume cheira Quando vem a chuva fina Salpicos no cume caem Formigas no cume entram Abelhas do cume saem Quando cai a chuva grossa A água do cume desce O barro do cume escorre O mato no cume cresce Então, quando cessa a chuva No cume volta a alegria Pois torna a brilhar de novo O Sol que no cume ardia No alto daquele cume Plantei uma roseira O vento no cume bate A rosa no cume cheira Quando vem a chuva fina Salpicos no cume caem Formigas no cume entram Abelhas do cume saem Quando cai a chuva grossa A água do cume desce O barro do cume escorre O mato no cume cresce Então, quando cessa a chuva No cume volta a alegria Pois torna a brilhar de novo O Sol que no cume ardia Pois torna a brilhar de novo O Sol que no cume ardia Pois torna a brilhar de novo O Sol que no cume ardia"
    data = string_to_bit_list(data)

    #separa o dado a ser enviado em diferentes pedacos, que serao transformados em frames
    num_of_frames = int(math.ceil(len(data)/100))
    data_pieces = separate_data(data, num_of_frames)


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
            except socket.timeout: #caso nao receba a resposta, chama a funcao trigger_timeout, que volta a janela
                print('timeout recieve')
                go_back.trigger_timeout()
                ack = '-1'

        #se todos os frames ja foram mandados
        if(frame_id >= num_of_frames):
            try:
                ack = c.recv(2048).decode()
                ack = separate_ack(ack)
                if ack == '-2': #se o client enviou -2, significa que ele processou todos os frames
                    print('client disconnected')
                    c.close()
                    break
            except socket.timeout:
                print("timeout recieve")
        else: #se ainda tem frames para mandar, manda
            try:
                c.sendall(list_to_string(make_frame(data_pieces[frame_id], num_of_frames, frame_id)).encode())
            except socket.timeout:
                print("send timeout")

if __name__ == '__main__':
    main()