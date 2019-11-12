# _*_ coding: utf-8 _*_
# Python program to implement server side of chat room.
import socket
import select
import sys

from thread import *

# create a socket "s" that is an AF_INET (internet socket)
# and uses SOCK_STREAM (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


port = int(sys.argv[1])
server_socket.bind(('', port))

server_socket.listen(20)

client_socket_list = []
username_list = []
BUFFER_SIZE = 2048
username = None
p_username = None


def clientthread(client_socket, client_address):
    client_socket.send("Welcome to this chatroom! \nPlease enter your username: ")

    username = client_socket.recv(BUFFER_SIZE)
    valid_name = naming_for_client(username, client_socket)
    while not valid_name:
        try:
            username = client_socket.recv(BUFFER_SIZE)
            valid_name = naming_for_client(username, client_socket)
        except:
            continue

    while True:
        try:
            # received message from client socket
            message = client_socket.recv(BUFFER_SIZE)
            if message:




            # FUNCTIONAL MESSAGE FOR CLIENT


                #PRIVATE MESSAGE
                if "#p" in message:
                    print "test private"
                    message = message.split("#p")
                    p_msg = message[1]
                    private_msg(p_msg, client_socket)




                #CREATE ROOM



                #SELECT ROOM




                #LEAVE ROOM







                # THIS BROADCAST ALL
                else:
                   message = "<" + username.rstrip() + "> " + message
                   send_to_client(message, client_socket)


            else:
                # remove connection if no message
                remove(username,client_socket)
        except:
            continue


def naming_for_client(username, client_socket):
    username_list_len = len(username_list)
    for i in range(username_list_len):
        if username == username_list[i]:
            client_socket.send("Please try a different name : ")
            return False

    username_list.append(username[:-1])
    return True


def send_to_client(message, client_socket):
    for clients in client_socket_list:
        if clients != client_socket:
            try:
                clients.send(message)
            except:
                remove(clients)

def private_msg(p_msg, client_socket):
    # p_msg contain the client destination and client_socket is the sender
    # in this case we need to find the client destination to send
    # and client socket to find username who send it
    p_msg = p_msg.split(":")
    print p_msg[0]
    p_username = p_msg[0]
    msg = p_msg[1]
    print msg


    # get the username sender from the client list
    j=0
    for client in client_socket_list:
        if client == client_socket:
            break
        j+=1

    # get the client socket for destination from socket list
    i=0
    for name in username_list:
        if name == p_username:
            client_socket_list[i].send(username_list[j]+':'+msg)
        i+=1




def remove(username,client_socket):
    for name in username_list:
        if name == username:
            username_list.remove(username)
    for client in client_socket_list:
        if client == client_socket:
            # remove client from the list
            client_socket_list.remove(client_socket)
            # close the connection
            client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    client_socket_list.append(client_socket)
    # prints the address of the user that just connected
    print(client_address[0] + " connected")
    start_new_thread(clientthread, (client_socket, client_address))

client.close()
server_socket.close()
