---
title: "suppressFiles.py"
date: 2021-01-24T17:06:08+01:00
draft: false
---

```python
#Script qui permet de supprimer les fichiers datant de plus de N jours.
#On lance un cron pour supprimer régulièrement ces fichiers.
#On élimine également les lignes correspondantes dans la base de données.

from subprocess import run
import sqlite3
from datetime import datetime, timedelta
from configparser import ConfigParser

parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

home = parser.get("paths", "home")
folder = parser.get("paths", "folder")
project = parser.get("paths", "project")
pathCamera_1 = parser.get("paths", "pathCamera_1")
pathCamera_2 = parser.get("paths", "pathCamera_2")
pathCamera_py = parser.get("paths", "pathCamera_py")
stock = parser.get("paths", "stock")
delay_delete = int(parser.get("frequences", "delay_delete"))
baseName = parser.get("paths", "baseName")
baseBackUp = parser.get("paths", "baseBackUp")

path_db = "{}/{}/{}".format(home, folder, project)

#commandes qui vont supprimer les fichiers de stock/
command_1 = "find {}/{} -type f -mtime +{} -delete".format(stock, pathCamera_1, delay_delete)
command_2 = "find {}/{} -type f -mtime +{} -delete".format(stock, pathCamera_2, delay_delete)
command_py = "find {}/{} -type f -mtime +{} -delete".format(stock, pathCamera_py, delay_delete)
command_del = "{} & {} & {}".format(command_1, commande_2, command_py)
run(command_del, shell=True)

#sauvegarder la base de données avant de la modifier (sécurité)
command_cp = "cp -f {}/{}/{}/{} {}/{}/{}/{}".format(home, folder, project, baseName, home, folder, project, baseBackUp)
run(command_cp, shell=True)

#suppression des lignes correspondantes de la base de données
dateDel = datetime.now() - timedelta(delay_delete)
conn = sqlite3.connect("{}/{}/{}/{}".format(home, folder, project, baseName))
c = conn.cursor()
c.execute("DELETE FROM camera_photo WHERE date <= ?", (dateDel,))
conn.commit()
conn.close()
```
