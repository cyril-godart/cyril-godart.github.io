import time
import threading

def sommeil():
    print("sommeil...")
    time.sleep(1)
    print("sommeil Terminé")

debut=time.time()

t1=threading.Thread(target=sommeil)
t1.start()

t2=threading.Thread(target=sommeil)
t2.start()

t1.join()
t2.join()

fin=time.time()
print(f"Durée : {round(fin-debut,3)}s")