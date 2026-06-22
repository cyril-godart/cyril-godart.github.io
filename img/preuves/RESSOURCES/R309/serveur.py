import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 52300 
ENDING_MSG = "q"

# Client's connections
connections = []

def handle_client_msg(connection: socket.socket, address: str) -> None:
    """
        Handle messages for one client
    """
    client_msg = ""
    while client_msg != ENDING_MSG:
        client_msg = connection.recv(1024).decode("utf8")
        print(f"[Client {address[0]}:{address[1]}] {client_msg}")
        # Message to broadcast to other clients.
        msg_to_send = f"[Client {address[0]}:{address[1]}] {client_msg}"
        broadcast(msg_to_send, connection)   
    # Client has left
    remove(connection, address)
    

def remove(connection: socket.socket, address: str) -> None:
    """
        Remove a client connection 
        (He/she has typed ENDING_MSG)
    """
    connections.remove(connection) 
    print(f"[Serveur] Client {address[0]}:{address[1]} vient de se déconnecter.")

def broadcast(message: str, connection: socket.socket) -> None:
    """
        Broadcast a client message to all other clients connected to the server
    """
    for client_connection in connections:
        if client_connection != connection:
            client_connection.send(message.encode("utf8"))

def server() -> None:
    """
        Main process: receive client's connections and
        start a new thread for each one to handle their messages
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(4)  # Accept 4 clients at most
        print("[Serveur] Serveur prêt.")        
        while True:
            connection, address = s.accept()
            print(f"[Serveur] Client {address[0]}:{address[1]} vient de se connecter.")
            connections.append(connection)
            threading.Thread(target=handle_client_msg, args=[connection, address]).start()

if __name__ == "__main__":
    server()