from GUI import GUI
from client import Client

SERVER_IP =  "192.168.2.27"
SERVER_PORT = 5124
PEER_PORT = 8500

if __name__ == "__main__":
    client = Client(SERVER_IP, SERVER_PORT, PEER_PORT)
    gui = GUI(client)
    gui.start()
