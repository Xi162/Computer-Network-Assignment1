import argparse
import sys
import threading
import sqlite3
import os

import fetch
import publish
import constants
import socket
import peerServer
from GUI import GUI
import agent

class Peer:
    def __init__(self):
        #create a local repo, which stores local path and fname
        # if os.path.exists("peer.db"):
        #     os.remove("peer.db")
        con = sqlite3.connect("peer.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)                                      
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS file_path(
                    fname text,
                    path text, 
                    primary key (fname))""")
        con.commit()
        res = cur.execute("SELECT name FROM sqlite_master")
        print(res.fetchall())
        con.close()

        #ping server for the main server to ping
        self.agent_server_thread = threading.Thread(target=agent.agent)
        self.agent_server_thread.daemon = True
        self.agent_server_thread.start()

        #peer server for other peers get file
        self.peer_server = peerServer.ThreadedTCPServer(("", constants.PEER_PORT), peerServer.ThreadedTCPRequestHandler)
        self.peer_server_thread = threading.Thread(target=self.peer_server.serve_forever)
        self.peer_server_thread.daemon = True
        self.peer_server_thread.start()

    def fetch(self, name):
        fetch.fetch(fname)

    def publish(self, fname, path):
        try:
            print("publishing", fname, path)
            publish.publish(fname, path)
        except socket.error as e:
            print("[Server Error] ", *e.args)
            return []
        except Exception as e:
            print('[Client Error]', *e.args)
            
            return []

    def fetch_local_list(self):
        con = sqlite3.connect("peer.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)                                      
        cur = con.cursor()
        res = cur.execute("SELECT * FROM file_path")
        return res.fetchall()

    def stop(self):
        self.agent_server_thread.join()
        self.peer_server_thread.join()
        self.peer_server.shutdown()

if __name__ == "__main__":
    peer = Peer()
    gui = GUI(peer)
    gui.start()
