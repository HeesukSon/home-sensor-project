import socket
import sys
import pickle
import json
import psycopg2

# Server addressing
PORT = 10000
hostname = socket.gethostname()    
IP_ADDR = socket.gethostbyname(hostname)

ip_room_map = open("room-map.json")
ip_room_map_json = json.load(ip_room_map)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (IP_ADDR, PORT)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# DB connection
db_conn = psycopg2.connect(dbname='homedata', user='postgres', host='localhost')
cursor = db_conn.cursor()

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
                data_json = json.loads(pickle.loads(data))

                print('Sound1: {}'.format(data_json['Sound1']))
                print('Sound2: {}'.format(data_json['Sound2']))
                print('Temperature: {}'.format(data_json['Temperature']))
                print('Humidity: {}'.format(data_json['Humidity']))
                print('Light: {}'.format(data_json['Light']))

                # timescale DB query execution
                insert_query = "INSERT INTO sensor_data (db_insert_time, room, data_gen_time, sound1, sound2, temperature, humidity, light) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                record_to_insert = ("now()", ip_room_map_json[data_json['From']], data_json['At'], "{"+','.join(map(str, data_json['Sound1']))+"}", "{"+','.join(map(str, data_json['Sound2']))+"}", data_json['Temperature'], data_json['Humidity'], data_json['Light'])
                cursor.execute(insert_query, record_to_insert)
                db_conn.commit()
                print("Record inserted successfully into the DB table")
            else:
                break
            
    finally:
        # Clean up the connection
        connection.close()

# Closing DB connection
cursor.close()
db_conn.close()