#!/usr/bin/python
class theSocket:
    """
    Default constructor class
    """
    def __init__(self, sock=None):
        #if sock does not exist, create it
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
        #if sock does exist, set it to itself
        else:
            self.sock = sock
    
    """
    Connect to the socket
    """
    def socketConnect(self, host, port):
        self.sock.connect((host, port))

    """
    Sending definition
    Takes in a message and sends it
    Raises an error if nothing is sent
    """
    def socketSend(self, message):
        totalbytessent = 0
        while totalbytessent < MESSAGELENGTH:
            sent = self.sock.send(message[totalbytessent:])
            if sent == 0:
                raise RuntimeError("socket connection has broken")
            totalbytessent = totalbytessent + sent

    """
    Receiving definition
    """
    def socketReceive(self):
        chunks = []
        bytes_received = 0
        while bytes_received < MESSAGELENGTH:
            chunk = self.sock.recv(min(MESSAGELENGTH - bytes_received, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
                chunks.append(chunk)
                bytes_received = bytes_received + len(chunk)
        return ''.join(chunks)
