import socket
import pickle
import select
HEADERSIZE = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 4101
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))

socket_list = [server]
clients = {}


def recieve(client):
    try:
        msg_header = client.recv(HEADERSIZE).decode(FORMAT)
        if msg_header:
            msg_length = int(msg_header)
            msg = client.recv(msg_length).decode(FORMAT)
            return {'header': msg_header, 'data': msg}
    except:
        return None


def send(client,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADERSIZE-len(send_length))
    client.send(send_length)
    client.send(message)    
    
def broadcast(notified_socket,msg):
    for client in clients:
        if client != notified_socket:
            send(client,msg)


def start():
    server.listen(100)
    print(f"Server is listening on {IP}")
    while True:
        #print(socket_list)
        read_sockets, write_sockets, err_sockets = select.select(
            socket_list, [], [])
        #print(read_sockets)
        #print("\n\n")
        for notified_socket in read_sockets:
            #print(notified_socket)
            if notified_socket == server:
                client, addr = server.accept()
                user = recieve(client)
                if user is False:
                    continue
                socket_list.append(client)
                clients[client] = user
                print(f"new connection from {addr} -> {user['data']}")

            else:
                msg = recieve(notified_socket)
                if msg == None:
                    print(
                        f"closed connection from {clients[notified_socket]['data']}")
                    socket_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                
                user = clients[notified_socket]
                print(f"Recieved message from {user['data']}: {msg['data']}")
                broadcast(notified_socket, user['data'] +"-> "+ msg['data'])

if __name__ == "__main__":
    start()
