import datetime
import time

print(f"[{datetime.datetime.now()}] Hallo aus dem Python-Docker-Container!")

while True:
    time.sleep(3)
    print("Fertig ausgeführt.")
