---
title: "runDjango.py"
date: 2021-01-24T17:23:20+01:00
draft: false
---

```python
"""Script python qui va lancer Django et rendre celui-ci accessible sur le réseau local
A indiquer dans le crontab en @reboot"""

import subprocess
from configparser import ConfigParser

parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

raspIp = parser.get("hosts", "raspIP")
home = parser.get("paths", "home")
folder =  parser.get("paths", "folder")
venv = parser.get("paths", "venv")
project = parser.get("paths", "project")
django_port = parser.get("hosts", "django_port")

#command = ". {}/{}/{}/bin/activate && python {}/{}/{}/manage.py runserver {}:{}".format(home, folder, venv, home, folder, project, raspIp, django_port)
command = ". {}/{}/{}/bin/activate && python {}/{}/{}/manage.py runserver 0.0.0.0:{}".format(home, folder, venv, home, folder, project, django_port)
subprocess.run(command, shell=True)
```
