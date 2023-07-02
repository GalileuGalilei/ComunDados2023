# first of all import the socket library
import socket	

# next create a socket object
s = socket.socket()		
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

#frame 
#flag = 01111110
def data_bit_stuffing(data):
    for i in range(len(data) - 6):
        if data[i : i+6] == ['0', '1', '1', '1', '1', '1']:
            data.insert(i+6, '0')

def integer_to_bit_list(integer):
    bits = bin(integer)[2:].zfill(8)  # Convert the ASCII value to a binary string
    return list(bits)

def string_to_bit_list(string):
    bit_list = []
    for char in string:
        byte = ord(char)  # Get the ASCII value of the character
        bits = bin(byte)[2:].zfill(8)  # Convert the ASCII value to a binary string
        bit_list.extend(list(bits))  # Add each bit to the bit list
    return bit_list

def make_frame(data):
    data_bit_stuffing(data)

    size = len(data)
    header = integer_to_bit_list(size)
    flag = ['0', '1', '1', '1', '1', '1', '1', '0']
    #por enquanto, 8 '0's
    trailer = ['0'] * 8

    bitarray = []
    bitarray += flag
    bitarray += header
    bitarray += data
    bitarray += trailer
    bitarray += flag

    return bitarray

def char_list_to_bytes(char_list):
    return bytes(char_list)

# a forever loop until we interrupt it or
# an error occurs
data = 'Chupa meu pau'
data = string_to_bit_list(data)
print(data)
data = make_frame(data)
str = ''

for i in range(len(data)):
    str += data[i]


while True:

    # wait for.
    c, addr = s.accept()	
    print ('Got connection from', addr )

    # send a thank you message to the client. encoding to send byte type.
    
    c.send(str.encode())

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break
