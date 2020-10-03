#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

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
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload) #Getting output file name
    if not payload:
        break
    payload = payload.decode() #Making output file name into string to check if it exists
    

    if exists(payload):
        framedSend(sock, b"True", debug) #If it exists, let user now and do not save
    else:
        framedSend(sock, b"False", debug) #File name doesn't exists, now get file information from client
        payload2 = framedReceive(sock, debug)
        if debug: print("rec'd: ", payload2)
        if not payload2:
            break
        framedSend(sock, payload2, debug)
        output = open(payload, 'wb')  #Write file information into the newly created output file
        output.write(payload2)
