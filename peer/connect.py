import socket
import constants
import json

<<<<<<< HEAD
def connect():
    connectSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connectSocket.settimeout(2)
=======
def connect(SERVER_IP):
    connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectSocket.settimeout(5)
>>>>>>> 00a6296fa1507a096b43d19d3e35488ef26175d6
    req = {
        "type": "connect"
    }
    reqJSON = bytes(json.dumps(req), "utf-8")
    try:
        connectSocket.connect((SERVER_IP, constants.SERVER_PORT))
        connectSocket.sendall(reqJSON)
        response, serverAddress = connectSocket.recvfrom(1024)
        response = json.loads(response.decode())
        if(response["type"] == "Connected"):
            print("Connected to server")
        else:
            raise Exception(response["data"])
        return True
    except Exception as e:
        print("Can not connect to server")
        print(e)
        return False
    