"""
Client Script.
Connects to the server and sends keywords to search.
"""
import socket
import sys
import os

# Add parent dir to path to access constants if needed, 
# or copy constants.py to client folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.constants import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, TERMINATION_MSG


def start_client():
    """
    Connects to the server and handles user input loop.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print(f"[Client] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
            s.connect((SERVER_HOST, SERVER_PORT))
            print("[Client] Connection established.")

            # Receive welcome message
            server_msg = s.recv(BUFFER_SIZE).decode("utf-8")
            print(f"[Server] {server_msg}")

            while True:
                user_input = input("[You] Enter keyword: ")
                s.send(user_input.encode("utf-8"))

                if user_input.lower() == TERMINATION_MSG:
                    print("[Client] Closing connection.")
                    break

                # Wait for large response (using a loop could be safer for huge data,
                # but buffer 4096 is usually enough for this exercise)
                response = s.recv(4096).decode("utf-8")
                print(f"[Server Response] {response}")

        except ConnectionRefusedError:
            print("[Error] Could not connect to the server. Is it running?")
        except Exception as e:
            print(f"[Error] {e}")


if __name__ == "__main__":
    start_client()