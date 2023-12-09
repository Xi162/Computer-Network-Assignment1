import socket
import json
import os
import base64
import io
from pathlib import Path

class Client:
    def __init__(self, SERVER_HOST, SERVER_PORT, PEER_PORT):
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.PEER_PORT = PEER_PORT

    def fetch_list(self):
        try:
            print("Fetching list...")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            req = {
                "type": "list"
            }

            client_socket.connect((self.SERVER_HOST, self.SERVER_PORT))
            reqJSON = json.dumps(req)
            client_socket.sendall(bytes(reqJSON, "utf-8"))

            received_bytes = client_socket.recv(1024)
            resJSON = b''
            while received_bytes:
                resJSON += received_bytes
                received_bytes = client_socket.recv(1024)

            resJSON = resJSON.decode('utf-8')
            res = json.loads(resJSON)

            client_socket.close()

            print("File list fetched.")
            return res["data"]
        except socket.error as e:
            print("[Server Error] ", *e.args)
        except Exception as e:
            print('[Client Error] ', *e.args)

    def download_file(self, selected_file, save_location):
        try: 
            if (selected_file == None or len(selected_file) <= 0):
                raise Exception("[File empty]", "Please choose a file")

            ips = self.get_ips(selected_file)
            self.load_file(ips, selected_file, save_location)
        except socket.error as e:
            print("[Server Error]", *e.args)
        except IOError as e:
            print("[Client Error]", "Cannot write file to file path.")
        except Exception as e:
            print('[Client Error] ', *e.args)

    def get_ips(self, filename):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)
        client_socket.connect((self.SERVER_HOST, self.SERVER_PORT))
        req = {
            "type": "fetch",
            "fname": filename
        }
        reqJSON = json.dumps(req)
        client_socket.sendall(bytes(reqJSON, "utf-8"))
        res = client_socket.recv(1024)
        res = res.decode()
        res = json.loads(res)
        client_socket.close()
        if res["code"] == 0:
            return res["data"]
        raise Exception("Client Error", res["data"])

    def load_file(self, ips, filename, save_location):
        peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        req = {
            "type": "load",
            "fname": filename
        }
        peerSocket.settimeout(1)
        for ip in ips:
            if os.path.exists(save_location):
                break
            try:
                peerSocket.connect((ip, self.PEER_PORT))
                reqJSON = json.dumps(req)
                peerSocket.sendall(bytes(reqJSON, "utf-8"))
                res = peerSocket.recv(1024)
                res = res.decode()
                res = json.loads(res)
                peerSocket.close()
                if res["code"] == 1:
                    raise FileNotFoundError(res["data"])
                elif res["code"] == 2:
                    raise RuntimeError(res["data"])
                elif res["code"] == 0:
                    with open(save_location, "w") as file:
                        file.write(res["data"])

                return
            except ConnectionError as e:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect((self.SERVER_HOST, self.SERVER_PORT))
                req = {
                    "type": "invalid_host",
                    "host": ip
                }
                reqJSON = json.dumps(req)
                clientSocket.sendall(bytes(reqJSON, "utf-8"))
                clientSocket.close()
                print("[Peer error] " + ip)
                print("Trying another peer...")
            except TimeoutError as e:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect((self.SERVER_HOST, self.SERVER_PORT))
                req = {
                    "type": "invalid_host",
                    "host": ip
                }
                reqJSON = json.dumps(req)
                clientSocket.sendall(bytes(reqJSON, "utf-8"))
                clientSocket.close()
                print("[Peer error] " + ip)
                print("Trying another peer...")
            except FileNotFoundError as e:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect((self.SERVER_HOST, self.SERVER_PORT))
                req = {
                    "type": "invalid_host_file",
                    "host": ip,
                    "fname": filename
                }
                reqJSON = json.dumps(req)
                clientSocket.sendall(bytes(reqJSON, "utf-8"))
                clientSocket.close()
                print("[Peer error] " + ip)
                print("Trying another peer...")
            except RuntimeError as e:
                print("[Peer error] " + ip)
                print("Trying another peer...")
        print("No peer available.")

    def shutdown(self):
        print("Shutting down...")

