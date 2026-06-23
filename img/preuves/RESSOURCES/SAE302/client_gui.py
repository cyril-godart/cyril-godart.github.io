import socket
import json
import threading
import os
import platform
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# Constants
DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 65432
BUFFER_SIZE = 4096
SOCKET_TIMEOUT = 3.0
DOCUMENTS_DIR = "documents"

class SimpleSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Client")
        self.root.geometry("800x600")
        
        self.client_socket = None
        self.is_connected = False
        
        # Variables
        self.ip_var = tk.StringVar(value=DEFAULT_IP)
        self.port_var = tk.StringVar(value=str(DEFAULT_PORT))
        self.query_var = tk.StringVar()
        self.regex_var = tk.BooleanVar(value=False)
        self.ext_vars = {
            "txt": tk.BooleanVar(value=True),
            "html": tk.BooleanVar(value=True),
            "pdf": tk.BooleanVar(value=True),
            "xlsx": tk.BooleanVar(value=True)
        }
        
        self.build_ui()

    def build_ui(self):
        # Connection Frame
        conn_frame = ttk.LabelFrame(self.root, text="Connection", padding=10)
        conn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(conn_frame, text="IP:").pack(side="left")
        ttk.Entry(conn_frame, textvariable=self.ip_var, width=15).pack(side="left", padx=5)
        ttk.Label(conn_frame, text="Port:").pack(side="left")
        ttk.Entry(conn_frame, textvariable=self.port_var, width=8).pack(side="left", padx=5)
        
        self.btn_connect = ttk.Button(conn_frame, text="Connect", command=self.connect_to_server)
        self.btn_connect.pack(side="left", padx=10)
        self.lbl_status = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.lbl_status.pack(side="left")
        
        # Search Frame
        search_frame = ttk.LabelFrame(self.root, text="Search", padding=10)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(search_frame, text="Query:").pack(side="left")
        ttk.Entry(search_frame, textvariable=self.query_var, width=30).pack(side="left", padx=5)
        ttk.Checkbutton(search_frame, text="Regex", variable=self.regex_var).pack(side="left", padx=5)
        
        for ext, var in self.ext_vars.items():
            ttk.Checkbutton(search_frame, text=f".{ext}", variable=var).pack(side="left", padx=2)
            
        self.btn_search = ttk.Button(search_frame, text="Search", command=self.start_search)
        self.btn_search.pack(side="left", padx=10)
        
        # Results Frame
        res_frame = ttk.Frame(self.root, padding=10)
        res_frame.pack(fill="both", expand=True)
        
        columns = ("file", "type", "location", "context")
        self.tree = ttk.Treeview(res_frame, columns=columns, show="headings")
        self.tree.heading("file", text="File")
        self.tree.heading("type", text="Type")
        self.tree.heading("location", text="Location")
        self.tree.heading("context", text="Context")
        
        self.tree.column("file", width=150)
        self.tree.column("type", width=50)
        self.tree.column("location", width=100)
        self.tree.column("context", width=300)
        
        scroll = ttk.Scrollbar(res_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        
        self.tree.bind('<Double-1>', self.on_double_click)

    def connect_to_server(self):
        try:
            ip = self.ip_var.get().strip()
            port = int(self.port_var.get().strip())
            
            if self.client_socket:
                self.client_socket.close()
                
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(SOCKET_TIMEOUT)
            self.client_socket.connect((ip, port))
            self.client_socket.settimeout(None)
            
            self.is_connected = True
            self.lbl_status.config(text="Connected", foreground="green")
            self.btn_connect.config(text="Reconnect")
        except Exception as e:
            self.is_connected = False
            self.lbl_status.config(text=f"Error: {e}", foreground="red")

    def start_search(self):
        if not self.is_connected:
            messagebox.showwarning("Warning", "Connect to server first.")
            return
            
        query = self.query_var.get().strip()
        if not query:
            return
            
        exts = [f".{k}" for k, v in self.ext_vars.items() if v.get()]
        if ".html" in exts:
            exts.append(".html")
            
        payload = {
            "query": query,
            "extensions": exts,
            "regex": self.regex_var.get()
        }
        
        self.btn_search.config(state="disabled")
        self.tree.delete(*self.tree.get_children())
        
        threading.Thread(target=self.send_search, args=(payload,), daemon=True).start()

    def send_search(self, payload):
        try:
            self.client_socket.sendall(json.dumps(payload).encode('utf-8'))
            self.client_socket.settimeout(SOCKET_TIMEOUT)
            
            received_data = b""
            while True:
                try:
                    chunk = self.client_socket.recv(BUFFER_SIZE)
                    if not chunk: break
                    received_data += chunk
                    if len(chunk) < BUFFER_SIZE: break
                except socket.timeout:
                    break
                    
            self.client_socket.settimeout(None)
            
            if received_data:
                results = json.loads(received_data.decode('utf-8'))
                self.root.after(0, lambda: self.populate_results(results))
                
        except Exception as e:
            self.is_connected = False
            self.root.after(0, lambda: self.lbl_status.config(text="Disconnected", foreground="red"))
            
        finally:
            self.root.after(0, lambda: self.btn_search.config(state="normal"))

    def populate_results(self, results):
        for item in results:
            self.tree.insert("", "end", values=(
                item.get('file', '?'),
                item.get('type', '?'),
                item.get('location', '?'),
                item.get('context', '?')
            ))

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            vals = self.tree.item(item_id, 'values')
            self.open_file(vals[0])

    def open_file(self, filename):
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, DOCUMENTS_DIR, filename)
        
        if not os.path.exists(path):
            messagebox.showerror("Error", f"File not found:\n{path}")
            return
            
        try:
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':
                subprocess.call(('open', path))
            else:
                subprocess.call(('xdg-open', path))
        except Exception as e:
            messagebox.showerror("OS Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleSearchApp(root)
    root.mainloop()