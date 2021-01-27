---
title: "RunCamera_1.py"
date: 2021-01-23T23:09:33+01:00
draft: false
---

```python
"""Script python qui va lancer la caméra 1 et permettre à mjpg-streamer de générer les flux et les images statiques
A indiquer dans le crontab en @reboot"""

import subprocess
from time import sleep
from configparser import ConfigParser

parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

cam_1_name = parser.get("camera", "cam_1_name")
cam_1_port = parser.get("camera", "cam_1_port")
cam_1_resol = parser.get("camera", "cam_1_resol")
cam_1_fps = parser.get("camera", "cam_1_fps")
mjpg_path = parser.get("paths", "mjpg")
delay_run=int(parser.get("frequences", "delay_run_Cam_1"))

sleep(delay_run)  #attente avant de lancer les commandes
command_1 = "cd {} && export LD_LIBRARY_PATH=. && ./mjpg_streamer -i 'input_uvc.so -r {} -fps {} -d /dev/v4l/by-id/{}' -o 'output_http.so -p {} -w {}/www'".format(mjpg_path,cam_1_resol, cam_1_fps, cam_1_name, cam_1_port, mjpg_path)
subprocess.run(command_1, shell=True)
```
