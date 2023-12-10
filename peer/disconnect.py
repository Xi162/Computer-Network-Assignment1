import socket
import constants
import json

def disconnect(SERVER_IP):
    connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectSocket.settimeout(2)
    req = {
        "type": "disconnect"
    }
    reqJSON = bytes(json.dumps(req), "utf-8")
    try:
        connectSocket.connect((SERVER_IP, constants.SERVER_PORT))
        connectSocket.sendall(reqJSON)
        response = connectSocket.recv(1024)
        response = json.loads(response.decode())
        if(response["code"] == 0):
            print("Disconnected from server")
        else:
            raise Exception(response["data"])
    except:
        print("Can not connect to server")
    