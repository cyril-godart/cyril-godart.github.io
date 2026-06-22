"""
Main Server Script.
Initializes the socket and handles client requests.
"""
import socket
import sys
import os

# Add the parent directory to sys.path to allow imports if running from server folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, TERMINATION_MSG
from file_searcher import search_all_files


def start_server():
    """
    Starts the TCP server, listens for connections, and processes
    search requests.
    """
    # 1) Creation of an IPv4/TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 2) Binding the socket
        try:
            s.bind((SERVER_HOST, SERVER_PORT))
        except OSError as e:
            print(f"Error binding to port {SERVER_PORT}: {e}")
            return

        # 3) Waiting for a client
        print(f"[Server] Server ready on {SERVER_HOST}:{SERVER_PORT}")
        s.listen(1)  # Accept 1 client at a time

        while True:
            # 4) Establishing the connection
            try:
                connection, address = s.accept()
                print(f"[Server] Client {address[0]}:{address[1]} connected.")

                welcome_msg = (f"Welcome! Enter a word to search in my files "
                               f"({TERMINATION_MSG} to quit).")
                connection.send(welcome_msg.encode("utf-8"))

                # 5) Chat loop
                while True:
                    client_msg = connection.recv(BUFFER_SIZE).decode("utf-8")
                    
                    if not client_msg or client_msg.lower() == TERMINATION_MSG:
                        print(f"[Server] Client {address} disconnected.")
                        break

                    print(f"[Client Request] Searching for: {client_msg}")
                    
                    # Perform the search using our module
                    search_result = search_all_files(client_msg)
                    
                    # Send result back
                    connection.send(search_result.encode("utf-8"))

                connection.close()
            except KeyboardInterrupt:
                print("\n[Server] Stopping server manually.")
                break
            except Exception as e:
                print(f"[Server] Error: {e}")


if __name__ == "__main__":
    start_server()