import socket
import threading
from queue import Queue
import sys
import datetime

# Paramètres de base
socket.setdefaulttimeout(0.5)
print_lock = threading.Lock()
target = input('Entrez l\'adresse IP à scanner: ')
log_file = f'scan_log_{target}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

# Fonctions
def write_log(message):
    with print_lock:
        with open(log_file, 'a') as file:
            file.write(message + '\n')

def get_banner(s):
    return s.recv(1024).decode().strip()

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((target, port))
        try:
            banner = get_banner(s)
            message = f'Port {port} est ouvert: {banner}'
            with print_lock:
                print(message)
        except:
            message = f'Port {port} est ouvert: Service inconnu'
            with print_lock:
                print(message)
        write_log(message)
    except:
        with print_lock:
            sys.stdout.write(f'\rScanning port {port}... ')
            sys.stdout.flush()
    finally:
        s.close()

def threader():
    while True:
        port = port_queue.get()
        if port is None:  # Signal pour arrêter le thread
            break
        scan_port(port)
        port_queue.task_done()

# Configuration du scanner
port_queue = Queue()
threads = []
for x in range(20):  # Ajuster le nombre de threads
    t = threading.Thread(target=threader)
    t.start()
    threads.append(t)

# Scan des ports
for port in range(1, 1025):
    port_queue.put(port)

# Arrêt des threads
for _ in range(len(threads)):
    port_queue.put(None)
for t in threads:
    t.join()
