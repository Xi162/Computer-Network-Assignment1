import sqlite3

def add_host(hostname, ip):
    con = sqlite3.connect("server.db")
    cur = con.cursor()
    cur.execute("INSERT INTO hosts(hostname, ip) VALUES (?, ?)", (hostname, ip))
    con.commit()
    con.close()
    print("Host {}: {} has been added".format(hostname, ip))
    
def add_cmd(args):
    try:
        add_host(args.hostname, args.ip)
    except Exception as e:
        print(e)