import socket
import json
import sys

# Constants
HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 4096
ENCODING = 'utf-8'

def get_boolean_input(prompt: str) -> bool:
    """ Get a boolean (y/n) input from the user. """
    while True:
        resp = input(prompt).strip().lower()
        if resp in ['y', 'yes', 'true', '1']:
            return True
        elif resp in ['n', 'no', 'false', '0', '']:
            return False
        print("Please enter y or n.")

def main():
    print("=== SEARCH ENGINE CLI ===")
    
    while True:
        print("\n" + "-"*30)
        # Get inputs
        query = input("Enter your search query (or 'quit' to exit): ").strip()
        if not query:
            print("Query cannot be empty.")
            continue
            
        if query.lower() in ('quit', 'exit'):
            print("Exiting CLI...")
            break

        ext_input = input("Enter extensions carefully separated by spaces (e.g. txt html pdf xlsx) or press Enter for all: ").strip()
        extensions = []
        if ext_input:
            extensions = [f".{ext}" if not ext.startswith('.') else ext for ext in ext_input.split()]
            if ".html" in extensions:
                extensions.append(".html")

        use_regex = get_boolean_input("Use regex? (y/N): ")

        payload = {
            "query": query,
            "extensions": extensions,
            "regex": use_regex
        }

        try:
            # Connect to server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connecting to server {HOST}:{PORT}...")
            client_socket.connect((HOST, PORT))
            
            # Send data
            print("Sending request...")
            client_socket.sendall(json.dumps(payload).encode(ENCODING))
            
            # Receive data
            received_data = b""
            while True:
                chunk = client_socket.recv(BUFFER_SIZE)
                if not chunk:
                    break
                received_data += chunk
                if len(chunk) < BUFFER_SIZE:
                    break
                    
            if received_data:
                results = json.loads(received_data.decode(ENCODING))
                print(f"\n--- {len(results)} RESULT(S) FOUND ---")
                for i, res in enumerate(results, 1):
                    print(f"\nResult #{i}:")
                    print(f"  File: {res.get('file', '?')}")
                    print(f"  Type: {res.get('type', '?')}")
                    print(f"  Location: {res.get('location', '?')}")
                    print(f"  Context: {res.get('context', '?')}")
            else:
                print("No data received from server.")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass

if __name__ == "__main__":
    main()
