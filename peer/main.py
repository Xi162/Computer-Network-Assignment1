import argparse
import sys
import threading
import sqlite3
import os

import fetch
import publish
import constants
import peerServer
import socket
from GUI import GUI

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

        #peer server for other peers get file
        self.server = peerServer.ThreadedTCPServer(("", constants.PEER_PORT), peerServer.ThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

        self.server_thread.start()

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
        self.server.shutdown()
        self.server_thread.join()
        self.server.server_close()

if __name__ == "__main__":
    peer = Peer()
    gui = GUI(peer)
    gui.start()
