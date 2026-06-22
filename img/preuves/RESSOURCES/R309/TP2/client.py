import socket

HOST = '127.0.0.1'
PORT = 65432

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Impossible de se connecter au serveur (est-il lancé ?)")
        return

    print("Connecté au serveur de Quiz !")

    while True:
        try:
            # Réception du message serveur (Question ou Résultat)
            msg = client.recv(4096).decode('utf-8')
            if not msg:
                break
            
            print(msg)

            # Si le message attend une réponse (contient "Votre réponse")
            if "Votre réponse" in msg:
                reponse = input("-> ")
                client.send(reponse.encode('utf-8'))
            
            # Détection de fin de jeu
            if "FIN DU QUIZ" in msg:
                break
                
        except Exception as e:
            print(f"Erreur : {e}")
            break

    client.close()
    print("Connexion fermée.")

if __name__ == "__main__":
    main()