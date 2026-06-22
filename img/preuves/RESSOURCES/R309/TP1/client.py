import socket

HOST, PORT = '127.0.0.1', 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        data = s.recv(1024).decode()
        if not data:
            break
            
        # Si le serveur demande une réponse, on utilise input()
        print(data, end='')
        if "reponse :" in data.lower() or "pseudo :" in data.lower():
            rep = input()
            s.sendall(rep.encode())