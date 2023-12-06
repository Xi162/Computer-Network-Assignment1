import socketserver
import sqlite3
import json
import datetime

def insert_file_host(host, file):
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    cur.execute("INSERT INTO file_host(host, file) VALUES (?, ?)", (host, file))
    con.commit()
    con.close()
    
def get_host(file):
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    res = cur.execute("SELECT host FROM file_host WHERE file=?", (file,))
    res = res.fetchall()
    res = list(map(lambda obj: obj[0], res))
    con.close()
    return res

def delete_file_host(host, file):
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    res = cur.execute("DELETE file_host WHERE host=? AND file=?", (host,file))
    res = res.fetchall()
    res = list(map(lambda obj: obj[0], res))
    con.close()
    return res

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        req = str(self.request.recv(1024), 'utf8')
        reqObj = json.loads(req)
        response = None
        if reqObj["type"] == "publish":
            try:
                insert_file_host(self.client_address[0], reqObj["filename"])
                response = {
                    "code": 0,
                    "data": "File {} has been recorded".format(reqObj["filename"])
                }
            except:
                response = {
                    "code": 1,
                    "data": "Server Error"
                }
        elif reqObj["type"] == "fetch":
            try:
                response = get_host(reqObj["filename"])
                response = {
                    "code": 0,
                    "data": response
                }
            except:
                response = {
                    "code": 1,
                    "data": "Server Error"
                }
        else:
            response = {
                "code": 2,
                "data": "Bad request"
            }
        response = json.dumps(response)
        response = bytes(response, 'utf8')
        print(response)
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    