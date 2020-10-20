#! /usr/bin/env python3

"""Lab 2 File Transfer
   Edgar Escobedo
   Professor David Pruitt & Eric Freudenthal
   MW 3:00 p.m. - 4:20 p.m.
   This lab assignment was created with the use of demos provided by the professors. 
   The lab involves a client and a server which communicated to each other to transfer files.
   In the first implementation the connection of multiple clients to a server was done by using 
   forking. In the second part Threads were introduced and the notion of Locks. Locks help to 
   avoid transferring files to the same place at the same time, which could cause errors. The
   lab also allows the use of a proxy to communicate between the client and the server as a 
   middle-man. The lab was done in collaboration with Zabdi Valenciana 

"""

# Echo client program
import socket, sys, re

from os.path import exists

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive



switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

file_to_send = input("type file to send : ")

if exists(file_to_send):
    file_copy = open(file_to_send, 'rb') #open file
    file_data = file_copy.read()    #save contents of file
    if len(file_data) == 0:
        print("cannot send empty file")
        sys.exit(0)
    else:
        file_name = input("give us file name ")
        framedSend(s, file_name.encode(), debug)
        file_exists = framedReceive(s, debug)
        file_exists = file_exists.decode()
        if file_exists == 'True':
            print("file already exists in server")
            sys.exit(0)
        else:            
            try:
                framedSend(s, file_data, debug)
            except:
                print("------------------------------")
                print("connection lost while sending.")
                print("------------------------------")
                sys.exit(0)
            try:
                framedReceive(s, debug)
            except:
                print("------------------------------")
                print("connection lost while receiving.")
                print("------------------------------")
                sys.exit(0)

else:
    print("file does not exist.")
    sys.exit(0)