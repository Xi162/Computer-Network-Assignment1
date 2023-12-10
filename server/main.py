import threading
import sqlite3
import mainServer
import os
import argparse
import sys
import constants

import ping
import discover
import add_host
import managementServer

#create and connect to sqlite database
# if os.path.exists("server.db"):
#     os.remove("server.db")
con = sqlite3.connect("server.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)                                      
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS hosts(
            ip text,
            hostname text, 
            online boolean  default(FALSE), 
            primary key(ip));""")
con.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS file_host(
            host text, 
            file text, 
            primary key(host, file),
            foreign key (host) REFERENCES hosts(ip) ON DELETE CASCADE ON UPDATE CASCADE)""")
con.commit()
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchall())
con.close()

#initialize server and server thread
server = mainServer.ThreadedTCPServer(("", constants.SERVER_PORT), mainServer.ThreadedTCPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True

NMP_server = managementServer.NMP_server(constants.NMP_PORT)
NMP_server_thread = threading.Thread(target=NMP_server.start)
NMP_server_thread.daemon = True

def prog_exit(args):
    server.shutdown()
    print("Server shutdown")
    # if os.path.exists("server.db"):
    #     os.remove("server.db")
    # else:
    #     print("The file does not exist")
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

#add host parser
publish_parser = subparser.add_parser("add", help="Add a host to a system")
publish_parser.add_argument("hostname", help="host name of the host")
publish_parser.add_argument("ip", help="ip address of the host")
publish_parser.set_defaults(func=add_host.add_cmd)

#exit parser
exit_parser = subparser.add_parser("exit", help="Exit the program")
exit_parser.set_defaults(func=prog_exit)

if __name__ == "__main__":
    print("Server listening on port", constants.SERVER_PORT)
    server_thread.start()
    
    print("NMP server listen on port", constants.NMP_PORT)
    NMP_server_thread.start()
    
    while True:
        user_input = input("> ")
        args = parser.parse_args(user_input.split())
        args.func(args)
