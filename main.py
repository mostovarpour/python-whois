# #!/usr/bin/env python

# import socket, os, re
# # from time import strftime

# """
# Want to use a server socket instead of a client socket so we can
# continually listen with it
# """
# serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# """
# Binding the socket to the local server
# (This would be changed to socket.gethostname() if this was public facing)
# We will use port 80 because, why not
# """
# serversocket.bind(('localhost', 8080))

# """
# Allow a max of 5 connect requests before refusing any
# outside connections
# """
# serversocket.listen(5)
# print "Success!"

class mysocket:
    """
    Default constructor class
    """
    def __init__(self, sock=None):
        #if sock does not exist, create it
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            print(sock)
        #if sock does exist, set it to itself
        else:
            self.sock = sock
            print(sock)
    
    """
    Connect to the socket
    """
    def connect(self, host, port):
        self.sock.connect((host, port))

    """
    Sending definition
    Takes in a message and sends it
    Raises an error if nothing is sent
    """
    def mysend(self, message):
        totalbytessent = 0
        while totalbytessent < MESSAGELENGTH:
            sent = self.sock.send(message[totalbytessent:])
            if sent == 0:
                raise RuntimeError("socket connection has broken")
            totalbytessent = totalbytessent + sent
            print totalbytessent
            print sent

    """
    Receiving definition
    """
    def myreceive(self):
        chunks = []
        bytes_received = 0
        while bytes_received < MESSAGELENGTH:
            chunk = self.sock.recv(min(MESSAGELENGTH - bytes_received, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
                chunks.append(chunk)
                bytes_received = bytes_received + len(chunk)
        return ''.join(chunks)
        print chunks