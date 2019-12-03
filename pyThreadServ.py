# https://github.com/micropython/micropython/issues/2916
# Python program to implement server side of chat room.
import time
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


# Actual room
room_list = []

# List contain names for rooms
roomname_list = []
username_list = []


BUFFER_SIZE = 2048
username = None
p_username = None


def clientthread(client_socket, client_address):
    global client_socket_list
    global room_list
    global roomname_list
    global username_list
    global BUFFER_SIZE


    client_socket.send("Welcome to this chatroom! \nPlease enter your username: ")


    # Receive client first name
    username = client_socket.recv(BUFFER_SIZE)

    valid_name = False

    if username:
        valid_name = naming_for_client(username, client_socket)
    else:
        remove(username,client_socket,client_address)

    while not valid_name:
        try:
            username = client_socket.recv(BUFFER_SIZE)
            valid_name = naming_for_client(username, client_socket)
        except:
            continue

    # casting username if it is a valid name
    username=username[:-1]

    while True:
        try:
            # received message from client socket
            message = client_socket.recv(BUFFER_SIZE)
            if message:




            # FUNCTIONAL MESSAGE FOR CLIENT


                #PRIVATE MESSAGE
                if "#p" in message:
                    message = message.split("#p")
                    p_msg = message[1]
                    private_msg(p_msg, client_socket)




                #CREATE ROOM
                elif "#cr:" in message:
                    roomname = message.split("#cr:")

                    # cast the actual roomname
                    roomname = roomname[1][:-1]
                    if roomname =='':
                        client_socket.send('Invalid room name')
                    else:
                        if create_room(roomname,username):
                            # print on server
                            print('Room '+roomname+' is created by '+username)
                            client_socket.send('Room '+roomname+' created. You have joined room '+roomname)
                        else:
                            client_socket.send("Can't create room. The room's name already exists")



                #MESSAGE MULTIPLE ROOMS
                elif "#msg "in message:
                    message = message.split("#msg ")
                    r_list = message[1].split("~")

                    # take last element to cast out the message
                    cast = r_list[-1].split(":")
                    # getting last room in the request room list from cast [0]
                    # cast [1] is the message to send
                    r_list[-1]=cast[0]
                    message = cast[1][:-1]
                    if message != '':
                        msg_to_room(r_list,message,username,client_socket)
                    else:
                        client_socket.send('Message has no contain :(')






                #LEAVE ROOM
                elif "#lr:" in message:
                    roomname = message.split("#lr:")

                    #cast the actual roomname
                    roomname = roomname[1][:-1]
                    if roomname =='':
                        client_socket.send('Invalid room name')
                    else:
                        if leave_room(roomname,username,client_socket):
                            pass
                        else:
                            client_socket.send("Can't leave room. The room's name does not exist")


                #JOIN ROOM
                elif "#jr:" in message:
                    roomname = message.split("#jr:")

                    #cast the actual roomname
                    roomname = roomname[1][:-1]
                    if roomname =='':
                        client_socket.send('Invalid room name')
                    else:
                        if join_room(roomname,username,client_socket):
                            pass
                        else:
                            client_socket.send("Can't join room. The room's name does not exist")

                #LIST MEMBERS IN THE ROOM
                elif "#lrm:" in message:
                    roomname = message.split("#lrm:")

                    # cast the actual roomname
                    roomname = roomname[1][:-1]
                    if roomname == '':
                        client_socket.send('Invalid room name')
                    else:
                        if list_room_member(roomname, client_socket):
                            pass
                        else:
                            client_socket.send("Can't list member in the room. The room's name does not exist")


                #LIST ALL THE ROOM
                elif "#lsr" in message:
                    i=1
                    for r_name in roomname_list:
                        client_socket.send(str(i)+')'+r_name+'\n')
                        i+=1

                #LIST ALL IN THE SERVER
                elif "#lsam" in message:
                    i = 1
                    for u_name in username_list:
                        client_socket.send(str(i) + ')' + u_name+'\n')
                        i += 1







                # THIS BROADCAST ALL
                else:
                   message = "<" + username.rstrip() + "> " + message
                   send_to_client(message, client_socket)


            else:
                # remove connection if no message
                remove(username,client_socket,client_address)
        except socket.error:
            continue


# Message to multiple rooms
def msg_to_room(r_list,message,username,client_socket):
    for r_name in r_list:
        # if there is a match room name sending the message else room not found
        if r_name in roomname_list:
            for name in room_list[roomname_list.index(r_name)]:
                if name in username_list:
                    client_socket_list[username_list.index(name)].send('Room ' + r_name + ' <' + username + '>:' + message)
        else:
            client_socket.send('Room ' + r_name+ ' does not exist')





def naming_for_client(username, client_socket):
    username_list_len = len(username_list)
    username=username[:-1]
    for i in range(username_list_len):
        if username == username_list[i]:
            client_socket.send("Please try a different name : ")
            return False

    username_list.append(username)
    return True

def list_room_member(roomname,client_socket):
    i=0
    thread_room_list = room_list
    for room_name in roomname_list:
        try:
            # find a matching room name
            if roomname == room_name:
                j=1
                for m_name in room_list[i]:
                    client_socket.send(str(j) + ')' + m_name+'\n')
                    j+=1
                return True
        except Exception as e:
            print(e)
        i+=1
    return False

def join_room(roomname,username,client_socket):
    i=0
    thread_room_list = room_list
    for room_name in roomname_list:
        try:
            # find a matching room name
            if roomname == room_name:
                #  see if the username in the room
                if username not in room_list[i]:
                    # adding username in the list
                    client_socket.send('You have joined ' + roomname)
                    room_list[i].append(username)
                else:
                    # username is in the room list already
                    client_socket.send('You have joined ' + roomname+' already')
                return True
        except Exception as e:
            print(e)
        i+=1
    return False


def leave_room(roomname,username,client_socket):
    roomname_list_len = len(roomname_list)
    for i in range(roomname_list_len):

        # find a matching room name
        if roomname == roomname_list[i]:

            #  the username if in the room
            try:
                room_list[i].remove(username)
            except ValueError:
                client_socket.send('You are not in room ' + roomname)
                return True

            client_socket.send('You left room ' + roomname)
            return True

    return False



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
            client_socket_list[i].send('(private)'+username_list[j]+':'+msg)
        i+=1


def create_room(roomname,username):
    roomname_list_len = len(roomname_list)
    for i in range(roomname_list_len):
        if roomname == roomname_list[i]:
            return False

    #adding room name in the list
    roomname_list.append(roomname)
    #adding client into the room list
    room_list.append([username])
    return True




def remove(username,client_socket,client_address):
    if username:
        print('<'+username+'>'+' disconnected')
    else:
        print(str(client_address)+' disconnected')

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
    try:
        client_socket, client_address = server_socket.accept()
        client_socket_list.append(client_socket)
        # prints the address of the user that just connected
        print(str(client_address) + " connected")
        start_new_thread(clientthread, (client_socket, client_address))
    except KeyboardInterrupt or socket.error:
        print('Server is shutting down ')
        time.sleep(0.1)
        sys.exit()
        server_socket.close()
