import socket

HEADER = 64
PORT =  8080
FORMAT = "utf-8"
DISCONNECT_MSG = "!disconnected"
SERVER = socket.gethostbyname(socket.gethostname()) #"192.168.0.150"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len)) #added space to be req len
    client.send(send_len)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("aaa")
input()
send("bbb")
input()
send(DISCONNECT_MSG)