import socket
import time
from poses import CONFIGURACIONS

# Dirección IP del robot UR
HOST = "10.10.73.23X"

# Puerto del servidor en el robot
PORT = 30002

# Scripts para abrir y cerrar la pinza
Abrir_pinza = 'pinza40UR3.py'
Cerrar_pinza = 'pinza10UR3.py'

# Función para enviar una trayectoria en espacio de configuraciones a la controladora del robot
def send_joint_path(path, sock):
    for joint_config in path:
        print(joint_config)
        sock.send(f"movej({joint_config}, a=0.5, v=0.5)".encode() + "\n".encode())
        time.sleep(3)

# Conexión via socket a la controladora del robot
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Trayectoria -- configuraciones (variables articulares, en radianes)
path = [
    [-0.4252,-2.3921,0.5604,-1.3436,1.6586,0.0059],
    [0.2353,-2.3921,0.5604,-1.3436,1.6586,0.0059],]



def moure_robot(source, goal, sock):
    path = [source, goal]
    send_joint_path(path, sock)
    
def cerrar_pinza(archivo, sock):
    with open(archivo, 'rb') as f: sock.sendall(f.read())
    time.sleep(1)

def abrir_pinza(archivo, sock):
    with open(archivo, 'rb') as f: sock.sendall(f.read())
    time.sleep(1)



with open('output_movement.txt', 'r') as file:
    a = file.readlines()
moves = a[-58:-10]

moves_clean = []
for m in moves:
    m = m.replace('step','').replace('  ','').replace('\n','').split(':')[1][1:].split()
    moves_clean.append(m)


for step in moves_clean:
    if step[0] == 'MOVER':
        init = CONFIGURACIONS[step[-2]]
        final = CONFIGURACIONS[step[-1]]
        moure_robot(init, final, sock)

    elif step[0] == 'PLACE':
        pos = CONFIGURACIONS[step[-2]]
        nivell = CONFIGURACIONS[step[-1]]
        cerrar_pinza(Abrir_pinza, sock)
    
    elif step[0] == 'PICK':
        pos = CONFIGURACIONS[step[-1]]
        cerrar_pinza(Cerrar_pinza, sock)

# Mensaje que se imprime cuando se finaliza la ejecución
# de la trayectoria
print("Trayectoria finalizada")

data = sock.recv(1024)

#tancar connexió
sock.close()# Se envia la trayectoria a la controladora del robot
