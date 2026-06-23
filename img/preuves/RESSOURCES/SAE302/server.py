import socket
import threading
import json
import search_tool

# Constants
HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 4096
ENCODING = 'utf-8'

def handle_client(conn: socket.socket, addr: tuple):
    """ Handle individual client connection. """
    print(f"Client connected: {addr}")
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            
            try:
                request = json.loads(data.decode(ENCODING))
                query = request.get('query', '')
                extensions = request.get('extensions', [])
                use_regex = request.get('regex', False)

                print(f"[{addr}] Searching for: '{query}'")
                
                # Perform the search
                results = search_tool.process_search(query, extensions, use_regex)
                
                # Send back the results as JSON
                response = json.dumps(results)
                conn.sendall(response.encode(ENCODING))
            except json.JSONDecodeError:
                print(f"[{addr}] Received invalid JSON.")
                break
    except Exception as e:
        print(f"[{addr}] Error: {e}")
    finally:
        conn.close()
        print(f"Client disconnected: {addr}")

def start_server():
    """ Start the server to listen for client connections. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except Exception as e:
        print(f"Server crashed: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()