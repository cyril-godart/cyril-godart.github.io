import concurrent.futures
import time

def sommeil(s):
    print("sommeil...")
    time.sleep(s)
    return f"sommeil Terminé"

debut=time.time()

with concurrent.futures.ThreadPoolExecutor() as executor :
    threads = []
    for i in range(1000):
        threads.append(executor.submit(sommeil,1))
    
    for thread in concurrent.futures.as_completed(threads):
        print(thread.result())
        

fin=time.time()
print(f"Durée : {round(fin-debut,3)}s")