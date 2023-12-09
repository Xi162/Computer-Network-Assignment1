import socket
import sqlite3
import constants
import json

def insert_repo(fname, path):
    con = sqlite3.connect("peer.db")
    cur = con.cursor()
    cur.execute("INSERT INTO file_path(fname, path) VALUES (?, ?)", (fname, path))
    con.commit()
    con.close()

def publish(fname, lname):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(5)
    clientSocket.connect((constants.SERVER_IP, constants.SERVER_PORT))
    req = {
        "type": "publish",
        "fname": fname
    }
    reqJSON = json.dumps(req)
    clientSocket.sendall(bytes(reqJSON, "utf8"))
    res = clientSocket.recv(1024)
    res = res.decode()
    res = json.loads(res)
    clientSocket.close()
    print(res)
    if res["code"] == 0:
        insert_repo(fname, lname)
    elif res["code"] == 1:
        raise RuntimeError(res["data"])
    elif res["code"] == 2:
        raise SyntaxError(res["data"])
    elif res["code"] == 3:
        print("File exists, can not publish")
