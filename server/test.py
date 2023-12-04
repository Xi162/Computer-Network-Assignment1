import socket as s
import json
import time

HOST = "LAPTOP-SCMCQCF9"
PORT = 5124

def send():
    clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    req = {
        "type": "heartbeat"
    }
    reqJSON = json.dumps(req)
    clientSocket.sendall(bytes(reqJSON, "utf8"))
    print(reqJSON)


send()
time.sleep(5.0)
send()

