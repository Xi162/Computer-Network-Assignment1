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

def publish(args):
    print(args.lname, args.fname)
    insert_repo(args.fname, args.lname)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((constants.SERVER_IP, constants.SERVER_PORT))
    req = {
        "type": "publish",
        "filename": args.fname
    }
    reqJSON = json.dumps(req)
    clientSocket.sendall(bytes(reqJSON, "utf8"))
    res = clientSocket.recv(1024)
    res = res.decode()
    res = json.loads(res)
    clientSocket.close()
    print(res)
    if res["code"] == 1:
        raise RuntimeError(res["data"])
    elif res["code"] == 2:
        raise SyntaxError(res["data"])
    return res