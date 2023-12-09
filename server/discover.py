import socket
import json

def discover_host(host):
    discoverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discoverSocket.settimeout(2)
    try:
        discoverSocket.connect((host, 8501))
        req = {
            "type": "discover"
        }
        reqJSON = json.dumps(req)
        discoverSocket.sendall(bytes(reqJSON, "utf-8"))
        res = discoverSocket.recv(1024)
        res = res.decode()
        print(res)
        res = json.loads(res)
        return res["list"]
    except ConnectionError:
        print("Discover failed")
        raise ConnectionError("Can not connect to peer")
    except TimeoutError:
        print("Discover failed")
        raise TimeoutError("Request timed out")
        
def discover_cmd(args):
    discover_host(args.host)


# discover("192.168.1.217")