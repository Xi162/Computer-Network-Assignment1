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
            "filename": filename
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

    def load_file(self, ips, file_name, save_location):
        if ips == None:
            raise Exception("File not found", "Cannot find file in the system.")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)
        req = {
            "type": "load",
            "filename": file_name
        }

        for ip in ips:
            print(f"Downloading from {ip}")
            client_socket.connect((ip, self.PEER_PORT))
            reqJSON = json.dumps(req)
            client_socket.sendall(bytes(reqJSON, "utf-8"))
            header = client_socket.recv(1024).decode('utf-8')
            header = json.loads(header) 

            if header['code'] == 0:
                file_length = header["length"]
                file_length = int(file_length)
                file_content=b''

                # For tracking purposes
                current_file_length=0

                with open(save_location, "wb") as file:
                    file_stream = client_socket.recv(1024)
                    while file_stream:
                        current_file_length += len(file_stream)
                        file.write(file_stream)
                        file_stream = client_socket.recv(1024)
                    file.flush()

                if os.path.getsize(save_location) < file_length:
                    if os.path.exists(save_location):
                        os.remove(save_location)
                    print(f"Download failed (length = {current_file_length}/{file_length}) ")
                    continue
                
                print(f"Download succeeded {file_name} (length = {current_file_length}/{file_length})")

                break
            else:
                print(f"Download failed {ip}")

        client_socket.close()

        if not os.path.exists(save_location):
            raise Exception("Cannot find file in the system.")

    def shutdown(self):
        print("Shutting down...")

