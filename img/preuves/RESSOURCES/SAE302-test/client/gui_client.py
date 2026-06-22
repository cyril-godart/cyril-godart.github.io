"""
Graphical User Interface (GUI) for the SAE3.02 Client.
Built with Tkinter (Standard Python Library).
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import sys
import os

# Ajout du dossier parent au path pour importer les constantes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server.constants import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, ENCODING_FORMAT, TERMINATION_MSG


class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SAE3.02 - File Search Client")
        self.root.geometry("600x700")

        self.client_socket = None
        self.connected = False

        # --- Frame: Connection ---
        conn_frame = ttk.LabelFrame(root, text="Connection", padding=10)
        conn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(conn_frame, text=f"Server: {SERVER_HOST}:{SERVER_PORT}").pack(side="left")
        self.btn_connect = ttk.Button(conn_frame, text="Connect", command=self.connect_to_server)
        self.btn_connect.pack(side="right")
        self.btn_disconnect = ttk.Button(conn_frame, text="Disconnect", command=self.disconnect_from_server, state="disabled")
        self.btn_disconnect.pack(side="right", padx=5)

        # --- Frame: Search Settings ---
        search_frame = ttk.LabelFrame(root, text="Search Settings", padding=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        # Keyword Input
        ttk.Label(search_frame, text="Keyword / Regex:").grid(row=0, column=0, sticky="w")
        self.entry_keyword = ttk.Entry(search_frame, width=40)
        self.entry_keyword.grid(row=0, column=1, padx=5, pady=5)
        # Bind Enter key to search
        self.entry_keyword.bind('<Return>', lambda event: self.send_search())

        # Filter Selection
        ttk.Label(search_frame, text="File Type:").grid(row=1, column=0, sticky="w")
        self.filter_var = tk.StringVar(value="all")
        
        filter_box = ttk.Frame(search_frame)
        filter_box.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Radiobutton(filter_box, text="All", variable=self.filter_var, value="all").pack(side="left")
        ttk.Radiobutton(filter_box, text="PDF", variable=self.filter_var, value="pdf").pack(side="left", padx=10)
        ttk.Radiobutton(filter_box, text="Excel", variable=self.filter_var, value="excel").pack(side="left")
        ttk.Radiobutton(filter_box, text="Text/HTML", variable=self.filter_var, value="text").pack(side="left", padx=10)

        # Search Button
        self.btn_search = ttk.Button(search_frame, text="Search", command=self.send_search, state="disabled")
        self.btn_search.grid(row=2, column=1, sticky="e", pady=10)

        # --- Frame: Results ---
        result_frame = ttk.LabelFrame(root, text="Results", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_area = scrolledtext.ScrolledText(result_frame, state="disabled", height=20)
        self.text_area.pack(fill="both", expand=True)

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log(self, message):
        """Adds a message to the result area."""
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")

    def connect_to_server(self):
        """Establishes connection to the server in a separate thread."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            
            self.log(f"[INFO] Connected to server.")
            self.btn_connect.config(state="disabled")
            self.btn_disconnect.config(state="normal")
            self.btn_search.config(state="normal")

            # Start listening thread
            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect: {e}")

    def disconnect_from_server(self):
        """Sends disconnect message and closes socket."""
        if self.connected:
            try:
                self.client_socket.send(TERMINATION_MSG.encode(ENCODING_FORMAT))
                self.client_socket.close()
            except:
                pass
            
            self.connected = False
            self.log("[INFO] Disconnected.")
            self.btn_connect.config(state="normal")
            self.btn_disconnect.config(state="disabled")
            self.btn_search.config(state="disabled")

    def send_search(self):
        """Formats and sends the search request."""
        if not self.connected:
            return

        keyword = self.entry_keyword.get().strip()
        file_filter = self.filter_var.get()

        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword.")
            return

        # Protocol format: filter|keyword
        msg = f"{file_filter}|{keyword}"
        try:
            self.client_socket.send(msg.encode(ENCODING_FORMAT))
            self.log(f"\n[SENDING] Filter: {file_filter} | Query: {keyword}")
            self.entry_keyword.delete(0, tk.END) # Clear input
        except Exception as e:
            self.log(f"[ERROR] Failed to send: {e}")
            self.disconnect_from_server()

    def receive_messages(self):
        """Listens for incoming messages from server."""
        while self.connected:
            try:
                msg = self.client_socket.recv(BUFFER_SIZE).decode(ENCODING_FORMAT)
                if not msg:
                    break
                self.log(msg)
            except:
                break
        
        if self.connected: # If loop broke unexpectedly
            self.disconnect_from_server()

    def on_closing(self):
        """Cleanup when closing window."""
        self.disconnect_from_server()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    # Optional: Apply a theme for better look
    # style = ttk.Style()
    # style.theme_use('clam') 
    app = ClientGUI(root)
    root.mainloop()