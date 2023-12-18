import json
import socket
import time
import constants

def send_heartbeat(connectSocket):
    while True:
            req = {
                "type": "heartbeat"
            }
            reqJSON = json.dumps(req)
            connectSocket.sendall(bytes(reqJSON, "utf8"))
            res = str(connectSocket.recv(1024), 'utf8')
            print(res)
            time.sleep(5.0)