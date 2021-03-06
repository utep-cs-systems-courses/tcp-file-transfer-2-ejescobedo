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

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            payload += b"!"             # make emphatic!
            framedSend(sock, payload, debug)