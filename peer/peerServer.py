import socketserver
import base64
import sqlite3
import json
import os
import mimetypes

def read_file_path(fname):
    con = sqlite3.connect("peer.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM file_path WHERE fname = ?", (fname,))
    path = res.fetchone()
    print(path)
    con.close()
    if not path:
        raise FileNotFoundError("File is no longer on server")
    elif not path[1]:
        raise FileNotFoundError("File is no longer on server")
    elif not os.path.exists(path[1]):
        raise FileNotFoundError("File not found")
    else:
        return path[1]

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        req = str(self.request.recv(1024), 'ascii')
        reqObj = json.loads(req)
        if reqObj["type"] == "load":
            print("LOAD")
            try:
                filepath = read_file_path(reqObj["filename"])
                print(reqObj["filename"],filepath)

                # Sent header
                header = {
                    "code": 0,
                    "type": mimetypes.guess_type(filepath),
                    "length": os.path.getsize(filepath),
                }
                response = bytes(json.dumps(header), 'utf8')
                self.request.sendall(response)

                # Sent data streams
                with open(filepath, "rb") as file:
                    file_bytes = file.read(1024)
                    while file_bytes:
                        self.request.sendall(file_bytes)
                        file_bytes = file.read(1024)
            except FileNotFoundError as e:
                print(e)
                response = {
                    "code": 1,
                    "data": e.args[0]
                }
                response = bytes(json.dumps(response), 'utf8')
                self.request.sendall(response)
            except Exception as e:
                print(e)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    