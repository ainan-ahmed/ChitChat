import socket
import select
import errno
import sys
import tkinter
HEADERSIZE = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 4101
FORMAT = 'utf-8'
username = ''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER, PORT))
# client.setblocking(False)
sockets_list = [sys.stdin, server]


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADERSIZE-len(send_length))
    server.send(send_length)
    server.send(message)


def recieve(connection):
    try:
        msg_header = connection.recv(HEADERSIZE).decode(FORMAT)
        if msg_header:
            msg_length = int(msg_header)
            msg = connection.recv(msg_length).decode(FORMAT)
            return msg
    except:
        return None
    

def start():
    print("----------------------------------------------")
    print("============WELCOME TO CHITCHAT===============")
    print("----------------------------------------------")
    username = input("Enter your username: ")
    send(username)
    while True:
        #print(username+"->",end="")
        #send(msg)
        read_sockets, write_sockets, err_sockets = select.select(
            sockets_list, [], [])
        for notified_socket in read_sockets:
            if notified_socket == server:
                msg = recieve(notified_socket)
                print(msg)
            else:
                message = sys.stdin.readline()
                send(message)
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
    server.close()
                

if __name__ == "__main__":
    start()
