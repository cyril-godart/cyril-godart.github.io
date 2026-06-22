import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 52300 
ENDING_MSG = "q"

def handle_server_msg(connection: socket.socket, client_prompt: str) -> None:
    """
        Receive and print messages sent by the server 
        while the client is connected
    """
    while True:
        try:
            server_msg = connection.recv(1024).decode("utf8")
            print(f"\n{server_msg}\n{client_prompt}", end="")
        except:
            # Client has left (ENDING_MSG has been typed)
            break

def client() -> None:
    """
        Main process: start a client and handle messages
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"** Connexion au Serveur {SERVER_HOST}:{SERVER_PORT} **")
        s.connect((SERVER_HOST, SERVER_PORT)) # Watch out the tuple!
        print(f"** Connexion établie (Tapez {ENDING_MSG} pour quitter)**")
        client_prompt = f"[Client {s.getsockname()[0]}:{s.getsockname()[1]} (Vous)] "
        # Create a thread to handle messages sent by the server
        threading.Thread(target=handle_server_msg, args=[s, client_prompt]).start()
        # Deal the client's inputs
        client_msg = ""
        while client_msg != ENDING_MSG:
            print(client_prompt, end="")
            client_msg = input()
            s.send(client_msg.encode("utf8"))
    
    # 4) Fermeture de la connexion : 
    print("** Fin connexion ** Au revoir **")

if __name__ == "__main__":
    client()