import socket as s
import json

HOST = "LAPTOP-SCMCQCF9"
PORT = 5124

clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
clientSocket.connect((HOST, PORT))
req = {
    "type": "fetch",
    "filename": "text.txt"
}
reqJSON = json.dumps(req)
print(reqJSON)
clientSocket.sendall(bytes(reqJSON, "utf8"))
res = clientSocket.recv(1024)
print(res.decode())
clientSocket.close()