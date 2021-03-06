import socket
import sys

PORT = 10000

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', PORT)
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
            data = connection.recv(16)
            
            if data:
                print('received: {}'.format(str(data)))
            else:
                print('no more data')
                break
            
    finally:
        # Clean up the connection
        connection.close()