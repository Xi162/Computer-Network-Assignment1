import threading
import sqlite3
import mainServer
import os
import argparse
import sys

import ping
import discover

#create and connect to sqlite database
# if os.path.exists("server.db"):
#     os.remove("server.db")
con = sqlite3.connect("server.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)                                      
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS file_host(
            host text, 
            file text, 
            primary key(host, file))""")
con.commit()
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchall())
con.close()

#initialize server and server thread
HOST, PORT = "", 5124
server = mainServer.ThreadedTCPServer((HOST, PORT), mainServer.ThreadedTCPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True

def prog_exit(args):
    server.shutdown()
    print("Server shutdown")
    if os.path.exists("server.db"):
        os.remove("server.db")
    else:
        print("The file does not exist")
    print("END")
    sys.exit(0)

#create parser for the CLI
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

#fetch parser
fetch_parser = subparser.add_parser("ping", help="Ping check a host")
fetch_parser.add_argument("host", help="host address to ping")
fetch_parser.set_defaults(func=ping.ping_cmd)

#publish parser
publish_parser = subparser.add_parser("discover", help="Discover which files a host keeps")
publish_parser.add_argument("host", help="host address to discover")
publish_parser.set_defaults(func=discover.discover_cmd)

#exit parser
exit_parser = subparser.add_parser("exit", help="Exit the program")
exit_parser.set_defaults(func=prog_exit)

if __name__ == "__main__":
    print("Server listening on port", PORT)
    server_thread.start()
    
    while True:
        user_input = input("> ")
        args = parser.parse_args(user_input.split())
        args.func(args)
