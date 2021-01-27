---
title: "RunCamera_2.py"
date: 2021-01-23T23:20:11+01:00
draft: false
---

```python
"""Script python qui va lancer la caméra 2 et permettre à mjpg-streamer de générer les flux et les images statiques
A indiquer dans le crontab en @reboot"""

import subprocess
from time import sleep
from configparser import ConfigParser

parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

cam_2_name = parser.get("camera", "cam_2_name")
cam_2_port = parser.get("camera", "cam_2_port")
cam_2_resol = parser.get("camera", "cam_2_resol")
mjpg_path = parser.get("paths", "mjpg")
delay_run=int(parser.get("frequences", "delay_run_Cam_2"))

sleep(delay_run)  #attente avant de lancer les commandes
command_2 = "cd {} && export LD_LIBRARY_PATH=. && ./mjpg_streamer -i 'input_uvc.so -r {} -d /dev/v4l/by-id/{}' -o 'output_http.so -p {} -w {}/www'".format(mjpg_path,cam_2_resol, cam_2_name, cam_2_port, mjpg_path)
subprocess.run(command_2, shell=True)
```
