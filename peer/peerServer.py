import socketserver
import sqlite3
import json
import os

def read_file_path(fname):
    con = sqlite3.connect("peer.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM file_path WHERE fname = ?", (fname,))
    path = res.fetchone()
    con.close()
    if not path:
        raise FileNotFoundError("File is no longer on server")
    elif not path[1]:
        raise FileNotFoundError("File is no longer on server")
    elif not os.path.exists(path[1]):
        raise FileNotFoundError("File not found")
    else:
        return path[1]
    
def delete_file(fname):
    con = sqlite3.connect("peer.db")
    cur = con.cursor()

    cur.execute("DELETE FROM file_path WHERE fname = ?", (fname,))
    con.commit()
    con.close()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        req = str(self.request.recv(1024), 'utf-8')
        reqObj = json.loads(req)
        if reqObj["type"] == "load":
            try:
                filepath = read_file_path(reqObj["fname"])

                with open(filepath, "r") as file:
                    file_content = file.read(1024)
                    
                res = {
                    "code": 0,
                    "data": file_content
                }
                response = bytes(json.dumps(res), 'utf-8')
                self.request.sendall(response)

            except FileNotFoundError as e:
                print('Error: ', e)
                delete_file(reqObj["fname"])
                response = {
                    "code": 1,
                    "data": e.args[0]
                }
                response = bytes(json.dumps(response), 'utf-8')
                self.request.sendall(response)
            except Exception as e:
                response = {
                    "code": 2,
                    "data": "Peer Error"
                }
                response = bytes(json.dumps(response), 'utf-8')
                self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    