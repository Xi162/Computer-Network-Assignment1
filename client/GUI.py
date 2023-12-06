import tkinter as tk
from screens.DownloadScreen import DownloadScreen

class GUI:
    def __init__(self, client):
        self.client = client
        self.root = tk.Tk()
    
    def start(self):
        self.root.title("Client")

        self.container = tk.Frame(self.root)
        self.container.grid_columnconfigure(0,weight=1)
        self.container.pack(fill="both", expand=True)

        # Screens
        self.download_screen = DownloadScreen(self.container, self)

        # Show screen
        self.show_screen(self.download_screen)

        self.root.geometry("400x300")
        self.root.mainloop()

    def show_screen(self, screen):
        screen.tkraise()

    def close(self):
        self.root.destroy()
