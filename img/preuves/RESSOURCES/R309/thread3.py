import time
import threading

def sommeil(s):
    print("sommeil...")
    time.sleep(s)
    print("sommeil Terminé")

debut=time.time()

threads=[]

for i in range(10000) :
    t = threading.Thread(target=sommeil,name=f"t{i}",args=[2])
    t.start()
    print(f"{t.name} lancé")
    threads.append(t)

for thread in threads:
    thread.join()

fin=time.time()
print(f"Durée : {round(fin-debut,3)}s")