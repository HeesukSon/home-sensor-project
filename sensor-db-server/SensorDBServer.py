import socket
import sys
import pickle

# Server addressing
PORT = 10000
hostname = socket.gethostname()    
IP_ADDR = socket.gethostbyname(hostname)        

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (IP_ADDR, PORT)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from {}'.format(client_address))

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            
            if data:
                print('received: {}'.format(pickle.loads(data)))
            else:
                break
            
    finally:
        # Clean up the connection
        connection.close()