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

# path_db = "{}/{}/{}".format(home, folder, project)
path_db = f'{home}/{folder}/{project}'

#commandes qui vont supprimer les fichiers de stock/
command_1 = ["find", f'{stock}/{pathCamera_1}', "-mtime", f'+{str(delay_delete)}', "-delete"]
command_2 = ["find", f'{stock}/{pathCamera_2}', "-mtime", f'+{str(delay_delete)}', "-delete"]
command_py = ["find", f'{stock}/{pathCamera_py}', "-mtime", f'+{str(delay_delete)}', "-delete"]
run(command_1)
run(command_2)
run(command_py)

#sauvegarder la base de données avant de la modifier (sécurité)
command_cp = ["cp", f'{path_db}/{baseName}', f'{path_db}/{baseBackUp}']
run(command_cp)

#suppression des lignes correspondantes de la base de données
dateDel = datetime.now() - timedelta(delay_delete + 1)
# conn = sqlite3.connect("{}/{}/{}/{}".format(home, folder, project, baseName))
conn = sqlite3.connect(f'{path_db}/{baseName}')
c = conn.cursor()
c.execute("DELETE FROM camera_photo WHERE date <= ?", (dateDel,))
conn.commit()
conn.close()
```
