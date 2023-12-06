import argparse
import sys
import threading
import sqlite3
import os

import fetch
import publish
import constants
import peerServer

#just to exit the program
def prog_exit(args):
    sys.exit(0)

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
server = peerServer.ThreadedTCPServer(("", constants.PEER_PORT), peerServer.ThreadedTCPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True

#create parser for the CLI
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

#fetch parser
fetch_parser = subparser.add_parser("fetch", help="Fetch parser")
fetch_parser.add_argument("fname", help="file name to fetch")
fetch_parser.set_defaults(func=fetch.fetch)

#publish parser
publish_parser = subparser.add_parser("publish", help="Publish parser")
publish_parser.add_argument("lname", help="path to the file")
publish_parser.add_argument("fname", help="alias file name when published")
publish_parser.set_defaults(func=publish.publish)

#exit parser
exit_parser = subparser.add_parser("exit", help="Exit the program")
exit_parser.set_defaults(func=prog_exit)

if __name__ == "__main__":
    print("Peer server listen on port", constants.PEER_PORT)
    server_thread.start()

    while True:
        user_input = input("> ")
        args = parser.parse_args(user_input.split())
        args.func(args)
