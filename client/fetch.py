import socket
import os
import json
import constants

def fetch(args):
    ips = getAdd(args.fname)
    

def getAdd(filename):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((constants.SERVER_IP, constants.SERVER_PORT))
    req = {
        "type": "fetch",
        "filename": filename
    }
    reqJSON = json.dumps(req)
    clientSocket.sendall(bytes(reqJSON, "utf8"))
    res = clientSocket.recv(1024)
    res = res.decode()
    res = json.loads(res)
    clientSocket.close()
    print(res)
    return res

def loadFile(ips, filename):
    peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    req = {
        "type": "load",
        "filename": filename
    }
    for ip in ips:
        if os.path.exists("./repo"+filename):
            break
        peerSocket.connect((ip, constants.PEER_PORT))
        reqJSON = json.dumps(req)
        peerSocket.sendall(bytes(reqJSON, "utf8"))
        res = peerSocket.recv(1024)
        res = res.decode()
        peerSocket.close()
        
    print(res)