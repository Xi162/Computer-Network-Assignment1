import tkinter as tk
from tkinter import filedialog, messagebox

class DownloadScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Choose a file", font=("Arial", 18))
        label.pack(pady=20,fill=tk.X)

        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.file_listbox.pack(fill=tk.X,pady=10, padx=32)

        list_file = self.controller.client.fetch_list()

        for file_name in list_file:
            self.file_listbox.insert(tk.END, file_name)

        download_button = tk.Button(self, text="Download", command=self.download_file)
        download_button.pack(pady=10, padx=10)

        self.grid(row=0,column=0,sticky=tk.NSEW)

    def download_file(self):
        selected_index = self.file_listbox.curselection()

        if not selected_index:
            messagebox.showinfo("Error", "Please select a file to download.")
            return

        selected_file = self.file_listbox.get(selected_index)

        # Choose file location and name to save
        save_location = filedialog.asksaveasfilename(
            title="Save file as",
        )

        if save_location:
            self.controller.client.download_file(selected_file, save_location)
        else:
            print("Operation canceled by the user.")
    
