#!/usr/bin/python

import socket
import os
import re
import redis
from IPy import IP
from os.path import expanduser
from time import strftime

#Will store the log file in the users home directory
LOGFILE = (expanduser("~") + '/whois-service-access.log')

redis_host = 'localhost'
redis_port = 6379
redis_password = ''


r = redis.StrictRedis(host=redis_host, port=redis_port,
                      password=redis_password, decode_responses=True)


def insert_into_redis(query_in):
    try:
        r.set(query_in, query_in)
    except Exception as e:
        print(e)


def lookup_from_redis(domain):
    try:
        for key in r.scan_iter(domain):
            return key
    except Exception as e:
        print(e)


#Check the input to make sure that it is something we can digest
def sanitize_input(query_in):
    try:
        query_in = query_in.lower()
        query_in = query_in.replace("..", ".")
        query_in = query_in.replace("/", "")
        query_in = query_in.replace("\\", "")
        # query_in = query_in.replace(n, "")
        return query_in
    except:
        print("Something went wrong while sanitizing the input")


#Check to see if the input is a valid IP address
def check_is_ip(query_in):
    try:
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if re.match(pattern, query_in):
            return True
        else:
            return False
    except:
        print("Something went wrong while checking the input for a valud IP")

#Now we want to check the input to ensure it is a valid domain name


def check_is_domain(query_in):
    try:
        #check to see if we have a tld and sld
        if (len(query_in.split(".")) == 1):
            return False
        #Split the domain on the .'s into different sections
        sections = query_in.split(".")
        regex = re.compile("^[a-z0-9\.-]+\n")
        for section in sections:
            if(section == ""):
                return False
            if(section[0] == "-"):
                return False
            if(section[-1] == "-"):
                return False
            if(regex.match(section + "\n")):
                pass
            else:
                return False
        return True
    except:
        print("Something went wrong while checking the input for a valid domain.")


def start_service():
    LISTEN_ADDRESS = "localhost"
    LISTEN_PORT = 8080
    MAX_QUERY_SIZE = 1024

    while True:
        #Create the socket for our service
        try:
            server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            print("Creating the socket for the WHOIS service...")
        except:
            print("Could not create the socket, something has gone wrong.")
            exit(2)

        #Try to bind the socket to our address and port
        try:
            server_socket.bind((LISTEN_ADDRESS, LISTEN_PORT))
            print("Service successfully bound to the socket...")
        except:
            print("Could not bind to the specified address (" +
                  LISTEN_ADDRESS + ") and/or port (" + str(LISTEN_PORT) + ").")
            print("The port might be in use or you might not have privileges.")
            exit(2)

        #Now allow up to five connections on the socket
        server_socket.listen(5)
        print("WHOIS service listening on " + LISTEN_ADDRESS +
              " over port " + str(LISTEN_PORT))

        #Accept a new connection
        socket_connection, socket_address = server_socket.accept()
        print("Successful connection from " + str(socket_address))

        #Start the main service loop
        while True:
            #Receive the data stream less than the MAX_QUERY_SIZE
            data_received = socket_connection.recv(MAX_QUERY_SIZE).decode()
            if not data_received:
                #If we do not receive any data then we need to break out the infinite while loop.
                #TODO Find a better way to do this
                break

            #Write the timestamp and IP address of who accessed the service to the log file
            try:
                file = open(LOGFILE, 'a+')
                file.write("[" + strftime("%Y/%m/%d %H:%M:%S") +
                           "] " + socket_address[0] + "\r\n")
                file.close()
            except IOError:
                print("There was a problem writing to the logfile.")

            #TODO Delete this before turning the assignment in
            print("Data from connected user: " + str(data_received))

            #insert the data we got from the user into redis

            #Sanitize the data we have received
            # sanitize_input(data_received)

            #TODO We would look up if we have the results of what we have stored in data_received
            # and then send them back to the client
            # socket_connection.send(data_received.encode())

            #TODO find out how many responses we are serving instead of just having a placeholder of 1
            number_of_responses = 1
            #TODO get the TLD instead of the placeholder
            TLD = "COM"

            #Create mock whois response
            response = "matthewo WHOIS server \r\n"
            response = response + \
                "for more information on matthewo, please hire him for the systems/devops engineer role \r\n"
            response = response + "This query returned " + \
                str(number_of_responses) + " object.\r\n"
            response = response + "\r\nrefer:\twhois.matthewo.com\r\n"
            response = response + "\r\ndomain:\t" + TLD + "\r\n"

            if (check_is_ip(data_received)):
                try:
                    response = response + (lookup_from_redis(data_received))
                    found = True
                    print response
                except:
                    print (
                        "Something went wrong while looking for the domain in redis")

                if (found == False):
                    response = response + "IPV4 address was not found in the database"

            # elif(check_is_domain(data_received)):
            else:
                #This is where we respond that the whois result was not found
                print("Not a valid ip or domain name\r\n")
                response = response + "\r\nThe domain was not found on this WHOIS server\r\n"
                socket_connection.send(response.encode())
                socket_connection.close
                break

            #Write the timestamp and IP address of who accessed the service to the log file
            try:
                file = open(LOGFILE, 'a+')
                file.write("[" + strftime("%Y/%m/%d %H:%M:%S") +
                           "] " + socket_address[0] + "\r\n")
                file.close()
            except IOError:
                print("There was a problem writing to the logfile.")

        socket_connection.send(response.encode())
        socket_connection.close


if __name__ == '__main__':
    start_service()
