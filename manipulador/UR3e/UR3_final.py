import socket
import time
from read_xml import confs
# Dirección IP del robot UR
HOST = "10.10.73.239"

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

pick_place_count = 2
for i in range(pick_place_count):
    send_joint_path(confs[f"path{i*3+1}"], sock)
    with open(Cerrar_pinza, 'rb') as f: sock.sendall(f.read())
    time.sleep(1)
    send_joint_path(confs[f"path{i*3+2}"], sock)
    with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
    time.sleep(1)
    send_joint_path(confs[f"path{i*3+3}"], sock)
   

# Mensaje que se imprime cuando se finaliza la ejecución
# de la trayectoria
print("Trayectoria finalizada")

data = sock.recv(1024)

# Se cierra la conexión
sock.close()