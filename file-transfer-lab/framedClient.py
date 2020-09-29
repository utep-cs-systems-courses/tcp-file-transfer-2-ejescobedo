#! /usr/bin/env python3

# Echo client program
import socket, sys, re

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
file_to_send = input("type file to send : ")


if exists(file_to_send):
    print("hello")
    file_copy = open(file_to_send, 'r') #open file
    file_data = file_copy.read()    #save contents of file
    #print(file_data)
    if len(s.encode('utf-8')) == 0:
        sys.exit(0)
    else:
        framedSend(s, file_data.encode(), debug)
        print("received:", framedReceive(s, debug))

else:
    sys.exit(0)