from functions import *
import socket
import select
import time


args = args_parser()

SERVER = socket.gethostbyname(socket.gethostname())
PORT = args.port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #set reuse the address

ADDR = (SERVER, PORT)
server.bind(ADDR)
server.listen()
sockets_list = [server]
clients = []

print('Listening for connections on: ', SERVER, '...')

wait_time = 3
com_time = 0
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == server:
            client_socket, client_address = server.accept()

            sockets_list.append(client_socket)
            clients.append(client_socket)
            print('Accepted new connection from: ', client_address, '...')

            msg_recv = recv_msg(client_socket)
            print(msg_recv[1])
            print('{} Uplink Transmission Successful'.format(com_time))
            time.sleep(wait_time)
            send_msg(client_socket, ['MSG_SERVER_TO_CLIENT', '{} Downlink Transmission successful'.format(com_time)])
            com_time += 1

        else:
            msg_recv = recv_msg(notified_socket)
            print('{} Uplink Transmission Successful'.format(com_time))
            time.sleep(wait_time)
            if msg_recv is False:
                print(f'Closed connection from: {notified_socket}...')
                sockets_list.remove(notified_socket)
                clients.remove(notified_socket)
                continue
            send_msg(notified_socket, ['MSG_SERVER_TO_CLIENT', '{} Downlink Transmission successful'.format(com_time)])
            com_time += 1

    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)
        clients.remove(notified_socket)

