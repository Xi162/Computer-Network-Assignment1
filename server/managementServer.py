import socket
import json
import sqlite3
import constants

def get_hosts():
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM hosts")
    res = res.fetchall()
    res = list(map(lambda obj: obj[0], res))
    return res

def get_hosts_info():
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM hosts")
    res = res.fetchall()
    res = list(map(lambda obj: (obj[0], obj[1]), res))
    return res

def update_online(host):
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    cur.execute("UPDATE hosts SET online = TRUE WHERE ip = ?", (host,))
    con.commit()
    con.close()

def update_offline(host):
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    cur.execute("UPDATE hosts SET online = FALSE WHERE ip = ?", (host,))
    con.commit()
    cur.execute("DELETE FROM file_host WHERE host = ?", (host,))
    con.commit()
    con.close()

class NMP_server:
    def __init__(self, port):
        self.port = port 

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(("", constants.NMP_PORT))
        while True:
            message, peerAddress = self.server.recvfrom(1024)
            if peerAddress[0] in get_hosts():
                message = json.loads(message.decode())
                if message["type"] == "connect":
                    try:
                        update_online(peerAddress[0])
                        response = {
                            "type": "Connected",
                            "data": "Update online success"
                        }
                    except Exception as e:
                        response = {
                            "type": "Error",
                            "data": "Server Error"
                        }
                        print(e)
                elif message["type"] == "disconnect":
                    try:
                        update_offline(peerAddress[0])
                        response = {
                            "code": "Disconnected",
                            "data": "Update offline success"
                        }
                    except:
                        response = {
                            "type": "Error",
                            "data": "Server Error"
                        }
                response = bytes(json.dumps(response), 'utf-8')
                self.server.sendto(response, peerAddress)  
                
     
         