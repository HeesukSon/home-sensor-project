import socket
import sys
import pickle
import json
import psycopg2
import threading

# DB connection
db_conn = psycopg2.connect(dbname='homedata', user='postgres', host='localhost')
cursor = db_conn.cursor()

ip_room_map = open("room-map.json")
ip_room_map_json = json.load(ip_room_map)

class ClientThread(threading.Thread):
    def __init__(self, cAddress, cSocket):
        threading.Thread.__init__(self)
        self.cSocket = cSocket
        self.cAddress = cAddress
        print("New connection added: {}".format(self.cAddress))
    def run(self):        
        while True:
            data = self.cSocket.recv(1024)
            
            if data:
                data_json = json.loads(pickle.loads(data))

                # timescale DB query execution
                insert_query = "INSERT INTO sensor_data (db_insert_time, room, data_gen_time, sound1, sound2, temperature, humidity, light, motion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                record_to_insert = ("now()", ip_room_map_json[data_json['From']], data_json['At'], "{"+','.join(map(str, data_json['Sound1']))+"}", "{"+','.join(map(str, data_json['Sound2']))+"}", data_json['Temperature'], data_json['Humidity'], data_json['Light'], data_json['Motion'])
                cursor.execute(insert_query, record_to_insert)
                db_conn.commit()
                print("Record inserted successfully into the DB table")
            else:
                break
        print("Client at {} disconnected...".format(self.cAddress))


# Server addressing
PORT = 10000
ALLOW_CONNECT = 5
hostname = socket.gethostname()    
IP_ADDR = socket.gethostbyname(hostname)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (IP_ADDR, PORT)
sock.bind(server_address)

# Listen for incoming connections
print('Server started! \nWaiting for a connection...')
while True:
    sock.listen(ALLOW_CONNECT)    
    cSocket, cAddress = sock.accept()

    newthread = ClientThread(cAddress, cSocket)
    newthread.start()

# Closing DB connection
cursor.close()
db_conn.close()