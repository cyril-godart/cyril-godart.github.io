import socket
import random
import os

def charger_questions(nom_fichier, nb=10):
    # Récupère le dossier où se trouve le script serveur.py
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    # Construit le chemin complet vers questions.txt
    chemin_complet = os.path.join(dossier_actuel, nom_fichier)
    
    with open(chemin_complet, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    
    pool = [l.strip().split(';') for l in lignes]
    return random.sample(pool, min(nb, len(pool)))

# charger_questions("questions.txt", nb=10)

def sauvegarder_score(nom, score):
    with open("scores.txt", "a") as f:
        f.write(f"{nom} : {score}/10\n")

# Configuration serveur
HOST, PORT = '127.0.0.1', 65432
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Serveur Quiz R&T démarré sur {PORT}...")

while True:
    conn, addr = server.accept()
    print(f"Client connecté : {addr}")
    
    try:
        conn.sendall(b"Entrez votre pseudo : ")
        pseudo = conn.recv(1024).decode().strip()
        
        questions = charger_questions("questions.txt",nb=10)
        score = 0
        
        for i, q in enumerate(questions):
            # Formatage : Question + choix
            enonce = f"\nQ{i+1}: {q[0]}\nA: {q[1]} B: {q[2]} C: {q[3]} D: {q[4]}\nVotre reponse : "
            conn.sendall(enonce.encode())
            
            reponse_client = conn.recv(1024).decode().strip().upper()
            
            if reponse_client == q[5]:
                score += 1
                conn.sendall(b"Correct !\n")
            else:
                conn.sendall(f"Faux ! La reponse etait {q[5]}\n".encode())
        
        bilan = f"\nTermine ! Score final de {pseudo} : {score}/10\n"
        conn.sendall(bilan.encode())
        sauvegarder_score(pseudo, score)
        
    except ConnectionResetError:
        print("Le client s'est déconnecté.")
    finally:
        conn.close()