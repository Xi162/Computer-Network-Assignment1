import socketserver
import base64
import sqlite3
import json
import os

def read_file(file):
    con = sqlite3.connect("peer.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM file_path")
    path = res.fetchone()
    con.close()
    if not path:
        raise FileNotFoundError("File is no longer on server")
    elif not path[1]:
        raise FileNotFoundError("File is no longer on server")
    elif not os.path.exists(path[1]):
        raise FileNotFoundError("File not found")
    else:
        f = open(path[1], "rb")
        res = f.read()
    return res

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        req = str(self.request.recv(1024), 'ascii')
        reqObj = json.loads(req)
        if reqObj["type"] == "load":
            try:
                print(reqObj)
                response = read_file(reqObj["filename"])
                response = {
                    "code": 0,
                    "data": base64.b64encode(response).decode('utf-8')
                }
                response = bytes(json.dumps(response), 'utf8')
                self.request.sendall(response)
            except FileNotFoundError as e:
                print(e)
                response = {
                    "code": 1,
                    "data": e.args[0]
                }
                response = bytes(json.dumps(response), 'utf8')
                self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    