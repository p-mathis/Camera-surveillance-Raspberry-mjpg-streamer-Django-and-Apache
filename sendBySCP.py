"""Script qui envoie en SCP une image prise depuis une autre raspberry vers la rasberry qui est le serveur Django"""

# https://stackoverflow.com/questions/250283/how-to-scp-in-python
# https://pypi.org/project/scp/

import paramiko
from scp import SCPClient
from datetime import datetime
from time import sleep, time
import subprocess

server = "192.168.1.50"
port = '22'
user = "pi"
password = 'HercuLe-AbattU-PenelOpe-AttenD-IthaqUe'

host = "127.0.0.1"
cam_port = "8081"
path_sender= "/var/www/stock/Camera_1"

path_host= "/var/www/stock/Camera_5"

print("lancement du scp")


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

date, name = datetime.now(),datetime.now().strftime("%d-%m_%H:%M:00")
command = 'wget http://{}:{}/?action=snapshot -O {}/{}.jpg'.format(host, cam_port, path_sender, name)
subprocess.run(command, shell=True)

sleep(8)

ssh = createSSHClient(server, port, user, password)

scp = SCPClient(ssh.get_transport())
print("connected")
scp.put(f'{path_sender}/{name}.jpg',f'{path_host}')
print('put')
scp.close()
print("closed / end")