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
        file_list = ["final","sd2.png"]
        return file_list

    def download_file(self, selected_file, directory):
        try: 
            if (selected_file == None or len(selected_file) <= 0):
                raise Exception("File empty", "Please choose a file")

            ips = self.get_ips(selected_file)
            self.load_file(ips, selected_file, directory)
            messagebox.showinfo("Download", "Download succeeded.")
        except socket.error as e:
            if (e.args[0] == 61):
                messagebox.showerror("Server Error", "The server is down.")
            else:
                messagebox.showerror("Server Error", e.args[1])
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
        return res["data"]
    
    def load_file(self, ips, filename, filepath):
        if ips == None:
            raise Exception("File not found", "Cannot find file in the system.")

        peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        req = {
            "type": "load",
            "filename": filename
        }

        self.create_folder(filepath)

        for ip in ips:
            if os.path.exists(filepath + "/" + filename):
                break
            peerSocket.connect((ip, self.PEER_PORT))
            reqJSON = json.dumps(req)
            peerSocket.sendall(bytes(reqJSON, "utf-8"))
            res = peerSocket.recv(1024)
            print(res)
            # res = res.decode('utf-8')
            # res = json.loads(res)
            # if res['code'] == 0:
            #     peerSocket.close()
            #     with open(filepath + "/" + filename, "wb") as file:
            #         file.write(base64.b64decode(res["data"].encode('utf-8')))
            with io.BytesIO(base64.b64decode(res)) as bio:
                bio.seek(0)
                img_data = bio.read()

                # Save the image data to a file
                with open(filepath + "/" + filename, "wb") as file:
                    file.write(img_data)

    def create_folder(self, file_path):
        if(file_path == '.'):
            return
        
        Path(file_path).mkdir(parents=True, exist_ok=True)

    def shutdown(self):
        print("Shutting down")
    
