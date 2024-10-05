import hashlib
import os
import threading
import socket
import json

threads = []
positive_result = []
ip = "127.0.0.1"
port = 8080

def get_cores():
    #a function that returns the number of cores
    return os.cpu_count()

def connect_to_server(ip, port):
    #a function that connects to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((ip, port))
        print("Connected to the server!")
        handle_worker(client_socket)
        
    finally:
        client_socket.close()
        print("connection closed")
        
def handle_worker(client_socket):
    #a function that manages the client's work with the server
    #sending the number of cores and recieving the target hashed number
    number_of_cores = str(get_cores())
    client_socket.send(number_of_cores.encode('utf-8'))
    hash_target = client_socket.recv(1024).decode('utf-8')

    while True:
        #a for loop that recieves the ranges to work on and creates a thread for each core to work on
        message_recieved = client_socket.recv(1024).decode('utf-8')
        if message_recieved == "found":
            print("found")
            break
        ranges_list = json.loads(message_recieved)

        for i in range(len(ranges_list)):
            #creating a thread for each core
            t = threading.Thread(target=crack_number, args=(ranges_list[i], hash_target))
            t.start()
            print("created a new thread")
            threads.append(t)

        for t in threads:
            t.join()

        if positive_result:
            #if the number was found, a message will be sent to the server
            message = f"found,{positive_result[0]}"
            client_socket.send(message.encode('utf-8'))
            break
        else:
            #sending a message to the server incase that the number was not in the range
            message = "notfound,"
            client_socket.send(message.encode('utf-8'))

def crack_number(range_list, target):
    #a function that searches for a hashed number in a specific number range to find the number
    start, end = range_list
    while start <= end:
        #changing the number to a specific format
        string_number = f"{start:010d}"
        
        #hashing the number and checking if the number is the hashed target
        hashed_number = hashlib.md5(string_number.encode())
        if hashed_number.hexdigest() == target:
            positive_result.append(start)
            print("the number was found!")
            return
        start += 1
        
    
    #in case that the number is not in the range
    print("the number was not found.")
    return

def main():
    connect_to_server(ip, port)

if __name__ == '__main__':
    main()