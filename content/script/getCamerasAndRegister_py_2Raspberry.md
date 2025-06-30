---
title: "GetCamerasAndRegister_py_2Raspberry"
date: 2025-06-30T17:22:00+02:00
draft: false
---

```python

"""Script python qui :
prend une photo depuis chacune des caméras
stocke cette photo dans le dossier ad hoc
modifie la base de données pour indiquer la date, la camera, le nom de la photo et le chemin du fichier
Dans la mesure où on est susceptible de prendre des photos rapprochées (moins de la minute), le cron est insuffisant
On fait donc une boucle while infinie avec le delta temps pour prendre les photos en fonction du paramète [frequences][capture] du fichier /etc/camera/configuration.ini."""

# Ajout d'une caméra supplémentaire

import subprocess
from datetime import datetime
from time import sleep, time
import sqlite3
from configparser import ConfigParser


parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

host = parser.get("hosts", "local")
stock = parser.get("paths", "stock")
pathCamera_1 = parser.get("paths", "pathCamera_1")
pathCamera_2 = parser.get("paths", "pathCamera_2")
pathCamera_py = parser.get("paths", "pathCamera_py")
home = parser.get("paths", "home")
folder = parser.get("paths", "folder")
project = parser.get("paths", "project")
baseName = parser.get("paths", "baseName")
cam_1_port = parser.get("camera", "cam_1_port")
cam_2_port = parser.get("camera", "cam_2_port")
cam_py_port = parser.get("camera", "cam_py_port")
capture = int(parser.get("frequences", "capture"))
appli = parser.get("paths", "appli")
script = parser.get("paths", "script")

path_1 = "{}/{}".format(stock, pathCamera_1)
path_2 = "{}/{}".format(stock, pathCamera_2)
path_py = "{}/{}".format(stock, pathCamera_py)

# Ajout d'une caméra suplémentaire - Ajout des variables
pathCamera_3 = parser.get("paths", "pathCamera_3")
cam_3_port = parser.get("camera", "cam_3_port")
path_3 = "{}/{}".format(stock, pathCamera_3)

# Ajout des caméras de la 2ème raspberry
pathCamera_5 = "Camera_5"
pathCamera_ir = "Camera_ir"


while True:
    sleep(capture -time() % capture)

    date, name = datetime.now(),datetime.now().strftime("%d-%m_%H:%M:%S")

    """On récupère les images snapshot et on les copie dans le dossier ad hoc"""

    command_1 = 'wget http://{}:{}/?action=snapshot -O {}/{}.jpg'.format(host, cam_1_port, path_1, name)
    command_2 = 'wget http://{}:{}/?action=snapshot -O {}/{}.jpg'.format(host, cam_2_port, path_2, name)
    command_py = 'wget http://{}:{}/?action=snapshot -O {}/{}.jpg'.format(host, cam_py_port, path_py, name)

    # Ajout d'une caméra supplémentaire : la commande
    command_3 = 'wget http://{}:{}/?action=snapshot -O {}/{}.jpg'.format(host, cam_3_port, path_3, name)

    #Modification de la commande pour la quatrième caméra
    #command = '{} & {} & {}'.format(command_1, command_2, command_py)  ANCIENNE COMMANDE
    command = '{} & {} & {} & {}'.format(command_1, command_2, command_py, command_3)

    subprocess.run(command, shell=True)

    """On copie dans la base de données les éléments relatifs aux images"""

    conn = sqlite3.connect("{}/{}/{}/{}".format(home, folder, project, baseName))
    c = conn.cursor()

    c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '1', ?, ?)".format(appli), (date, name, pathCamera_1))
    c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '2', ?, ?)".format(appli), (date, name, pathCamera_2))
    c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '3', ?, ?)".format(appli), (date, name, pathCamera_py))

    # Ajout de la commande pour la quatrième caméra
    c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '4', ?, ?)".format(appli), (date, name, pathCamera_3))

    # Ajout des caméras de la 2ème raspberry
    c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '5', ?, ?)".format(appli), (date, name, pathCamera_5))
    c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '6', ?, ?)".format(appli), (date, name, pathCamera_ir))


    conn.commit()
    conn.close()

#si la boucle True s'interrompt, le script est relancé
#command_replay = "python3 {}/getCamerasAndRegister.py".format(script)
#si la boucle True s'interrompt, la raspberry est reboutée
command_replay = "sudo reboot"

subprocess.run(command_replay, shell=True)


```