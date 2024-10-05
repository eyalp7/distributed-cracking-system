import socket
import json
import threading

#global variables that we will need later
IP = "127.0.0.1"
PORT = 8080

active_cores = 0
active_connections = 0
max_numbers_per_core = 10000000000 // 20

hash_target = "EC9C0F7EDCC18A98B1F31853B1813301"
has_found = False
ranges_list = []

lock = threading.Lock()

def update_ranges_list():
    #a function that updates the ranges list to contain ranges for cores to work on
    global ranges_list
    numbers_per_core = 10000000000 // active_cores
    if numbers_per_core > max_numbers_per_core:
        ranges_list = [[core * max_numbers_per_core, (core + 1) * max_numbers_per_core] for core in range(active_cores)]
    else:
        ranges_list = [[core * numbers_per_core, (core + 1) * numbers_per_core] for core in range(active_cores)]

def start_server(host='127.0.0.1', port=12345):
    #a function that starts the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(20)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
    finally:
        server_socket.close()

def get_client_ranges(number_of_cores):
    #a function that returns a list to send to the client to work on
    if number_of_cores > len(ranges_list):
        return [ranges_list.pop() for i in range(len(ranges_list))]
    return [ranges_list.pop() for i in range(number_of_cores)]

def handle_client(conn, addr):
    #a function that handles the connection with the client
    global active_cores, active_connections, has_found
    active_connections += 1
    print(f"Established connection from {addr}")
    print(f"current connections: {active_connections}")

    try:
        #the client sends the number of cores it has
        number_of_cores = int(conn.recv(1024).decode('utf-8'))
        active_cores += number_of_cores
        conn.send(hash_target.encode('utf-8'))
        update_ranges_list()
        
        while True:
            print(ranges_list)
            #a loop that sends the client new ranges everytime to work on
            with lock:
                if has_found:
                    conn.send(("found").encode('utf-8'))
                    break
            
            #sending the client new ranges to work on
            if not ranges_list:
                break
            client_ranges = get_client_ranges(number_of_cores)
            conn.send(json.dumps(client_ranges).encode('utf-8'))
            #recieving the results of the client
            header, message = conn.recv(1024).decode('utf-8').split(",")
            print(f"{header}, {message}")

            if header == 'found':
            #in case that the number was found
                with lock:
                    has_found = True
                print(f"The number is: {message}")
            elif header == 'quit':
            #in case that the client wants to quit
                break
    finally:
        #closing the connection
        conn.close()
        print(f"Connection with {addr} closed.")

def main():
    server_socket = start_server(IP, PORT)

if __name__ == "__main__":
    main()
