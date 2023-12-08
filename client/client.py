from tkinter import messagebox
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
            file_list = []

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

            print(len(received_bytes))

            resJSON = resJSON.decode('utf-8')
            res = json.loads(resJSON)

            client_socket.close()

            return res["data"]
        except socket.error as e:
            messagebox.showerror("Server Error", e.args[1])
        except Exception as e:
            if (len(e.args) > 1):
                messagebox.showerror(e.args[0], e.args[1])
            else:
                messagebox.showerror("Client Error", "Something went wrong, please try again!")

    def download_file(self, selected_file, save_location):
        try: 
            if (selected_file == None or len(selected_file) <= 0):
                raise Exception("File empty", "Please choose a file")

            ips = self.get_ips(selected_file)
            self.load_file(ips, selected_file, save_location)

            messagebox.showinfo("Download", "Download succeeded.")
        except socket.error as e:
            messagebox.showerror("Server Error", e.args[1])
        except IOError as e:
            messagebox.showerror("Client Error", "Cannot write file to file path.")
        except Exception as e:
            print(e)
            if (len(e.args) > 1):
                messagebox.showerror(e.args[0], e.args[1])
            else:
                messagebox.showerror("Client Error", "Something went wrong, please try again!")

    def get_ips(self, filename):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((self.SERVER_HOST, self.SERVER_PORT))
        req = {
            "type": "fetch",
            "filename": filename
        }
        reqJSON = json.dumps(req)
        clientSocket.sendall(bytes(reqJSON, "utf-8"))
        res = clientSocket.recv(1024)
        res = res.decode()
        res = json.loads(res)
        clientSocket.close()
        if res["code"] == 0:
            return res["data"]
        raise Exception("Client Error", res["data"])

    def load_file(self, ips, file_name, save_location):
        if ips == None:
            raise Exception("File not found", "Cannot find file in the system.")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        req = {
            "type": "load",
            "filename": file_name
        }

        for ip in ips:
            client_socket.connect((ip, self.PEER_PORT))
            reqJSON = json.dumps(req)
            client_socket.sendall(bytes(reqJSON, "utf-8"))
            header = client_socket.recv(1024).decode('utf-8')
            header = json.loads(header) 
            file_length = header["length"]
            file_length = int(file_length)

            if header['code'] == 0:
                file_content=b''

                # For tracking purposes
                current_file_length=0

                with open(save_location, "wb") as file:
                    file_stream = client_socket.recv(1024)
                    while file_stream:
                        current_file_length += len(file_stream)
                        file.write(file_stream)
                        file_stream = client_socket.recv(1024)
                        print("Downloading " + str(current_file_length) + "/" + str (file_length) + "... ", flush=True)
                    file.flush()

                if os.path.getsize(save_location) < file_length:
                    if os.path.exists(save_location):
                        os.remove(save_location)
                    raise Exception("Server Error", "Connection Interrupted.")

                break

        client_socket.close()

        if not os.path.exists(save_location):
            # TODO: Do something when no file exists
            raise Exception()

    def shutdown(self):
        print("Shutting down")

