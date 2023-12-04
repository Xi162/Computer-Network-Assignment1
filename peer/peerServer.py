import socketserver
import base64
import sqlite3
import json
import os

def read_file(file):
    con = sqlite3.connect("peer.db")
    cur = con.cursor()
    res = cur.execute("SELECT path FROM file_path WHERE fname = ?", (file,))
    path = res.fetchone()
    print(path)
    con.close()
    if not path[0]:
        raise FileNotFoundError("File is no longer on server")
    elif not os.path.exists(path[0]):
        raise FileNotFoundError("File not found")
    else:
        f = open(path[0], "r")
        res = f.read()
    return res

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        req = str(self.request.recv(1024), 'ascii')
        reqObj = json.loads(req)
        if reqObj["type"] == "load":
            try:
                response = read_file(reqObj["filename"])
                response = {
                    "code": 0,
                    "data": response
                }
                response = bytes(json.dumps(response), 'utf8')
                self.request.sendall(response)
            except FileNotFoundError as e:
                response = {
                    "code": 1,
                    "data": e
                }
                response = bytes(json.dumps(response), 'utf8')
                self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    