# _*_ coding: utf-8 _*_
# Python program to implement server side of chat room. 
import socket 
import select 
import sys
from thread import *

# create a socket "s" that is an AF_INET (internet socket)
# and uses SOCK_STREAM (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
 
port = int(sys.argv[1])  
s.bind(('', port)) 

s.listen(20) 

clnt_online = [] 
clnt =None 

def clientthread(clnt, ap):
    clnt.sendall("Welcome to this chatroom!")
    while True:
        try:
            message = clnt.recv(1024)
            if message:
                print "<" + ap[0] + "> " + message
                message_to_send = "<" + ap[0] + "> " + message
                for clients in clnt_online:
                    if clients!=ap:
                        try:
                            clients.send(message)
                        except:
                            clients.close()
                            remove(clients) 

        except: continue
        
while True:
	
    clnt, ap = s.accept()
    clnt_online.append(clnt)
  
      # prints the address of the user that just connected 
    print ap[0] + " connected"
	
    start_new_thread(clientthread,(clnt,ap))

clnt.close()
s.close()
  
  
