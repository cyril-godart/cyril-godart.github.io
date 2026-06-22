import time
import threading

def sommeil():
    print("sommeil...")
    time.sleep(1)
    print("sommeil Terminé")

debut=time.time()

threads=[]

for i in range(10000) :
    t = threading.Thread(target=sommeil,name=f"t{i}")
    t.start()
    print(f"{t.name} lancé")
    threads.append(t)

for thread in threads:
    thread.join()

fin=time.time()
print(f"Durée : {round(fin-debut,3)}s")