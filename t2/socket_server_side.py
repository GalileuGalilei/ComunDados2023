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

data = 'Thank you for connecting'.encode()

#frame 
#flag = 01111110
def data_bit_stuffing(data):
    for i in range(len(data) - 6):
        if data[i : i+6] == ['0', '1', '1', '1', '1', '1']:
            data.insert(i+6, '0')

def int_to_bit_list(num):
    binary_str = bin(num)[2:] 
    return list(binary_str)

def make_frame(data):
    data_bit_stuffing(data)

    size = len(data)
    header = int_to_bit_list(size)
    flag = ['0', '1', '1', '1', '1', '1', '1', '0']
    #por enquanto, 8 '0's
    trailer = [['0'] * 8]

    bitarray = []
    bitarray += flag
    bitarray += header
    bitarray += data
    bitarray += trailer
    bitarray += flag

    return bitarray

# a forever loop until we interrupt it or
# an error occurs
while True:

    # wait for.
    c, addr = s.accept()	
    print ('Got connection from', addr )

    # send a thank you message to the client. encoding to send byte type.
    var = 43
    
    c.send(data)

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break
