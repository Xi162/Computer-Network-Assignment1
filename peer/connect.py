import socket
import constants
import json

def connect():
    connectSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connectSocket.settimeout(5)
    req = {
        "type": "connect"
    }
    reqJSON = bytes(json.dumps(req), "utf-8")
    try:
        connectSocket.sendto(reqJSON, (constants.SERVER_IP, constants.NMP_PORT))
        response, serverAddress = connectSocket.recvfrom(1024)
        response = json.loads(response.decode())
        if(response["type"] == "Connected"):
            print("Connected to server")
        else:
            raise Exception(response["data"])
    except Exception as e:
        print("Can not connect to server")
        print(e)
    