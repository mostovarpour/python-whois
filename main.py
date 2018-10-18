#!/usr/bin/python

import socket, os, re
from os.path import expanduser
from time import strftime
# from netaddr import IPAddress, IPNetwork

#Will store the log file in the users home directory
LOGFILE = (expanduser("~") + '/whois.log')

def whois_service():
    LISTEN_ADDRESS = "localhost"
    LISTEN_PORT = 8080
    MAX_QUERY_SIZE = 1024

    #Create the socket for our service
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Creating the socket for the WHOIS service...")
    except:
        print("Could not create the socket, something has gone wrong.")
        exit(2)

    #Try to bind the socket to our address and port
    try:
        server_socket.bind((LISTEN_ADDRESS, LISTEN_PORT))
        print("Service successfully bound to the socket...")
    except:
        print("Could not bind to the specified address (" + LISTEN_ADDRESS + ") and/or port (" + str(LISTEN_PORT) + ").")
        print("The port might be in use or you might not have privileges.")
        exit(2)

    #Now allow up to five connections on the socket
    server_socket.listen(5)
    print("WHOIS service listening on " + LISTEN_ADDRESS + " over port " + str(LISTEN_PORT))

    #Accept a new connection
    socket_connection, socket_address = server_socket.accept()
    print("Successful connection from " + str(socket_address))
    
    #Start the main service loop
    while True:
        #Receive the data stream less than the MAX_QUERY_SIZE
        data_received = socket_connection.recv(1024).decode()
        if not data_received:
            #If we do not receive any data then we need to break
            break
        print("Data from connected user: " + str(data_received))

        #TODO We would look up if we have the results and then send them back to the client
        socket_connection.send(data_received.encode())
        LOGFILE = "[" + strftime("%d/%m/%Y %H:%M:%S") + "] " + socket_address[0] + " - "

    socket_connection.close

if __name__ == '__main__':
    whois_service()