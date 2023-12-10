from GUI import GUI
from client import Client
import argparse

<<<<<<< HEAD
SERVER_IP =  "171.232.187.254"
=======
>>>>>>> 00a6296fa1507a096b43d19d3e35488ef26175d6
SERVER_PORT = 5124
PEER_PORT = 8500

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", type=str, default='localhost', help="Specify the port number")
    args = parser.parse_args()

    client = Client(args.server, SERVER_PORT, PEER_PORT)
    gui = GUI(client)
    gui.start()
