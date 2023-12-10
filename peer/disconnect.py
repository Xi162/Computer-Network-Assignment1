import socket
import constants
import json

def disconnect():
    connectSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connectSocket.settimeout(2)
    req = {
        "type": "disconnect"
    }
    reqJSON = bytes(json.dumps(req), "utf-8")
    try:
        connectSocket.sendto(reqJSON, (constants.SERVER_IP, constants.NMP_PORT))
        response, serverAddress = connectSocket.recvfrom(1024)
        response = json.loads(response.decode())
        if(response["type"] == "Disconnected"):
            print("Disconnected from server")
        else:
            raise Exception
    except:
        print("Can not connect to server")
    