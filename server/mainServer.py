import socketserver
import sqlite3
import json

def insert_file_host(file, host):
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    cur.execute("INSERT INTO file_host VALUES (?, ?)", (file, host))
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

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        req = str(self.request.recv(1024), 'ascii')
        reqObj = json.loads(req)
        if reqObj["type"] == "publish":
            insert_file_host(reqObj["filename"], self.client_address[0])
            response = bytes("File {} has been recorded".format(reqObj["filename"]), 'utf8')
            self.request.sendall(response)
        elif reqObj["type"] == "fetch":
            response = json.dumps(get_host(reqObj["filename"]))
            response = bytes(response, "utf8")
            self.request.sendall(response)
        else:
            response = "Hello im listening"
            self.request.sendall(response.encode())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    