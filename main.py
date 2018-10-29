#!/usr/bin/python

import socket
import threading
import SocketServer
import os
import re
import sys
import signal
import pymysql
import subprocess
from os.path import expanduser
from time import strftime

# will store the log file in the users home directory
# probably want to put this in /var/log/ on a nix system
LOGFILE = (expanduser("~") + '/whois-service-access.log')

# variables for our mysql connection
MYSQL_HOST = 'localhost'
MYSQL_USER = 'python_user'
MYSQL_PASS = sys.argv[1]
MYSQL_DB = 'python_db'
MYSQL_CHARSET = 'utf8mb4'

# read an ip address from mysql
def read_ip(ip):
    mysql_connection = pymysql.connect(host=MYSQL_HOST,
                                    user=MYSQL_USER,
                                    password=MYSQL_PASS,
                                    db=MYSQL_DB,
                                    charset=MYSQL_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with mysql_connection.cursor() as cursor:
            sql = "SELECT `ip_address`, `registrant_contact`, `admin_contact`, `tech_contact` FROM `ips` where `ip_address`=%s"
            cursor.execute(sql, (ip))
            result = cursor.fetchone()
            return result
    except:
        print("Something went wront reading an IP from the database")
    mysql_connection.close()


# read a domain name from mysql
def read_domain(domain):
    mysql_connection = pymysql.connect(host=MYSQL_HOST,
                                    user=MYSQL_USER,
                                    password=MYSQL_PASS,
                                    db=MYSQL_DB,
                                    charset=MYSQL_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with mysql_connection.cursor() as cursor:
            sql = "SELECT `domain_name`, `registrant_contact`, `admin_contact`, `tech_contact` FROM `domains` where `domain_name`=%s"
            cursor.execute(sql, (domain))
            result = cursor.fetchone()
            return result
    except:
        print("Something went wrong reading a domain from the database")
    mysql_connection.close()


# check to see if the input is a valid IP address
def check_is_ip(query_in):
    try:
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if re.match(pattern, query_in):
            return True
        else:
            return False
    except:
        print("Something went wrong while checking the input for a valud IP")


# now we want to check the input to ensure it is a valid domain name
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

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    # our main service
    def handle(self):
        MAX_QUERY_SIZE = 1024

        #Receive the data stream less than the MAX_QUERY_SIZE
        try:
            self.data_received = self.request.recv(MAX_QUERY_SIZE)
        except Exception as e:
            print ("Caught exception socket.error : %s" % e)
        
        # if not self.data_received:
        #     #If we do not receive any data then we need to break out the while loop.
        #     break

        #Write the timestamp and IP address of who accessed the service to the log file
        try:
            file = open(LOGFILE, 'a+')
            file.write("[" + strftime("%Y/%m/%d %H:%M:%S") +
                        "] " + self.client_address[0] + "\r\n")
            file.close()
        except IOError:
            print("There was a problem writing to the logfile.")

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

        # sanitize the input!!!!! Was getting weird escape characters on the end of data_received before this.
        escapes = ''.join([chr(char) for char in range(1, 32)])
        self.data_received = self.data_received.translate(None, escapes)

        # check to see if the data received is an IP address
        if (check_is_ip(self.data_received)):
            # if the response from the db is not null then parse it and add it to the response
            if (read_ip(self.data_received) is not None):
                response_from_db = read_ip(self.data_received)
                ip_address = response_from_db["ip_address"]
                reg_contact = response_from_db["registrant_contact"]
                admin_contact = response_from_db["admin_contact"]
                tech_contact = response_from_db["tech_contact"]
                response = response + "IP: " + ip_address + "\r\n"
                response = response + "Registrant Contact: " + reg_contact + "\r\n"
                response = response + "Admin Contact: " + admin_contact + "\r\n"
                response = response + "Technical Contact: " + tech_contact + "\r\n"
                self.request.sendall(response)
                self.request.close()

            # let client know the IP was not found
            else:
                # print("The IP was not found on this whois server")
                response = response + "\r\nThe IP was not found on this WHOIS server\r\n"
                self.request.sendall(response)
                self.request.close()

        # check to see if the data received is a domain name
        elif(check_is_domain(self.data_received)):
            # if the response from the db is not null then parse it and add it to the response
            if (read_domain(self.data_received) is not None):
                response_from_db = read_domain(self.data_received)
                domain_name = response_from_db["domain_name"]
                reg_contact = response_from_db["registrant_contact"]
                admin_contact = response_from_db["admin_contact"]
                tech_contact = response_from_db["tech_contact"]
                response = response + "Domain: " + domain_name + "\r\n"
                response = response + "Registrant Contact: " + reg_contact + "\r\n"
                response = response + "Admin Contact: " + admin_contact + "\r\n"
                response = response + "Technical Contact: " + tech_contact + "\r\n"
                self.request.sendall(response)
                self.request.close()

            # let the client know the domain was not found
            else:
                # print("The DOMAIN was not found on this whois server")
                response = response + "\r\nThe domain was not found on this WHOIS server\r\n"
                self.request.sendall(response)
                self.request.close()
        else:
            #This is where we respond that the whois result was not found
            # print("Not a valid ip or domain name\r\n")
            response = response + "\r\nThe domain was not found on this WHOIS server\r\n"
            self.request.sendall(response)
            self.request.close()

        #Write the timestamp and IP address of who accessed the service to the log file
        try:
            file = open(LOGFILE, 'a+')
            file.write("[" + strftime("%Y/%m/%d %H:%M:%S") +
                        "] " + self.client_address[0] + "\r\n")
            file.close()
        except IOError:
            print("There was a problem writing to the logfile.")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

if __name__ == '__main__':
    # variables for our serversocket connection
    LISTEN_ADDRESS = "localhost"
    LISTEN_PORT = 8080
    try:
        server = ThreadedTCPServer((LISTEN_ADDRESS, LISTEN_PORT), ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        print ("Server loop running in thread:", server_thread.name)
    except KeyboardInterrupt:
        print ("Something went wrong while trying to start the multithreaded server.")
        sys.exit()
    
    # bash_command = "whois -h localhost -p 8080 test.com"
    # run_bash_command = subprocess.check_output(['bash', '-c', "whois -h localhost -p 8080 test.com"])
    # print ("Current thread:", server_thread.name)
    # client(LISTEN_ADDRESS, LISTEN_PORT, subprocess.check_output(['bash', '-c', "whois -h localhost -p 8080 test.com"]))

    # print ("Current thread:", server_thread.name)
    # client(LISTEN_ADDRESS, LISTEN_PORT, subprocess.check_output(['bash', '-c', "whois -h localhost -p 8080 test0.com"]))

    # print ("Current thread:", server_thread.name)
    # client(LISTEN_ADDRESS, LISTEN_PORT, subprocess.check_output(['bash', '-c', "whois -h localhost -p 8080 test1.com"]))

    # server.shutdown()
    # server.server_close()