# _*_ coding: utf-8 _*_
# Python program to implement server side of chat room.
import socket
import select
import sys
from thread import *

# create a socket "s" that is an AF_INET (internet socket)
# and uses SOCK_STREAM (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


port = int(sys.argv[1])
s.bind(('', port))

s.listen(20)

clnt_online = []
room = []
clnt = None


def clientthread(clnt, ap):
    clnt.sendall("Welcome to this chatroom!")
    while True:
        try:
            message = clnt.recv(1024)

            # split message into diffrent fields
            parsed = message.split("~")

            if message:

                # Parse username and message
                print "<" + parsed[0] + "> " + parsed[1]

                ap = parsed[0];
                print("name of ap: ", ap)
                # append username to message being sent
                message_to_send = "<" + parsed[0] + "> " + parsed[1]

                # Check to see if private message char found
                if ":" in parced[1]:
                    user_select = parsed[1].split
                    print user_select

                send_to_chat(message_to_send)

        except:
            continue


def create_a_room(clnt):


def send_to_chat(message_to_send):
    for clients in clnt_online:
        if clients != ap:
            try:
                clients.send(message_to_send)
            except:
                clients.close()
                remove(clients)


while True:
    clnt, ap = s.accept()
    clnt_online.append(clnt)

    # prints the address of the user that just connected
    print ap[0] + " connected"

    start_new_thread(clientthread, (clnt, ap))

clnt.close()
s.close()

