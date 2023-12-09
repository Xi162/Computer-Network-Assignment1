import threading
import sqlite3
import mainServer
import os
import time
from GUI import GUI

HOST, PORT = "", 5124
class Server:
    def __init__(self):
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
        self.server = mainServer.ThreadedTCPServer((HOST, PORT), mainServer.ThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

        self.server_thread.start()

    def fetch_local_list(self):
        try:
            list_file = mainServer.list_files()
            if list_file == None:
                return []

            return list_file
        except socket.error as e:
            print("[Server Error] ", *e.args)
        except Exception as e:
            print('[Client Error]', *e.args)

    def ping(self, hostname):
        try:
            print("Ping: " + hostname)
            return True
        except socket.error as e:
            print("[Server Error] ", *e.args)
            return False
        except Exception as e:
            print('[Client Error]', *e.args)
            return False 

    def discover(self, hostname):
        try:
            print("Discover: " + hostname)
            return [
                "file1",
                "file2",
            ]
        except socket.error as e:
            print("[Server Error] ", *e.args)
        except Exception as e:
            print('[Client Error]', *e.args)

    def stop(self):
        self.server_thread.join()
        self.server.shutdown()

        if os.path.exists("server.db"):
            os.remove("server.db")
        else:
            print("The file does not exist")


if __name__ == "__main__":
    server = Server()
    gui = GUI(server)
    gui.start()

    time.sleep(2)
