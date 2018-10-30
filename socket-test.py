#!/usr/bin/python

import SocketServer

class TCPServer(SocketServer.BaseRequestHandler):
    def run_service(self):
        MAX_QUERY_SIZE = 1024
        self.data = self.request.recv(MAX_QUERY_SIZE).strip()
        print "{} write: ".format(self.client_address[0])
        print self.data
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    LISTEN_ADDRESS = "localhost"
    LISTEN_PORT = 8080
    server = SocketServer.TCPServer((LISTEN_ADDRESS, LISTEN_PORT), TCPServer)
    server.serve_forever()