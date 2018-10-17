#!/usr/bin/python

import TheSocket
import socket, os, re
from os.path import expanduser
from time import strftime
# from netaddr import IPAddress, IPNetwork

#Environment variables for the server
LISTEN_ADDRESS = "localhost"
LISTEN_PORT = 8080
MAX_QUERY_SIZE = 128

#Will store the log file in the users home directory
LOGFILE = (expanduser("~") + '/log/')

#Create the socket
TheSocket.socketConnect()
try:
    theSocket.bind((LISTEN_ADDRESS, LISTEN_PORT))
except IOError:
    print("Could not bind to the specified address and/or port.")
    print("The port might be in use or you might not have privileges.")
    exit(2)
