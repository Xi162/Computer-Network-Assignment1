import socketserver
import sqlite3
import json

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        req = str(self.request.recv(1024), 'ascii')
        reqObj = json.loads(req)
        if reqObj["type"] == "load":
            try:
                f = open(reqObj["filename"], "r")
            except:
                res = "no"
            response = f.read()
            response = bytes(response, 'utf8')
            self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    