# source --> //https://www.youtube.com/watch?v=3QiPPX-KeSc

import socket
import threading #every client one thread

HEADER = 64
PORT =  8080
SERVER = socket.gethostbyname(socket.gethostname()) #192.168.0.150
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!disconnected"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #type of adress to accept(family), straming data tru socket (type)
server.bind(ADDR)

def handler_client(conn, addr): #handling each client
    print(f"[NEW CONN] {addr} connected")

    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT) #how many bytes to recieve for actual msg
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(HEADER).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
             
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()