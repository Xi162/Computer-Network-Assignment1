import threading
import sqlite3
import mainServer
import os

#create and connect to sqlite database
if os.path.exists("server.db"):
    os.remove("server.db")
con = sqlite3.connect("server.db")
cur = con.cursor()
cur.execute("CREATE TABLE file_host(file, host)")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())
con.close()

#initialize server and server thread
HOST, PORT = "", 5124
server = mainServer.ThreadedTCPServer((HOST, PORT), mainServer.ThreadedTCPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True

if __name__ == "__main__":
    print("Server listening on port", PORT)
    server_thread.start()

    user_input = input("> ")

    if(user_input == "exit"): 
        server.shutdown()
        print("Server shutdown")
        
    server_thread.join()
    if os.path.exists("server.db"):
        os.remove("server.db")
    else:
        print("The file does not exist")
    print("END")