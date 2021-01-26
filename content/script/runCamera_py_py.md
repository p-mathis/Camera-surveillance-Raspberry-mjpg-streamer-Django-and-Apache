---
title: "RunCamera_py.py"
date: 2021-01-23T23:20:18+01:00
draft: false
---

```python
"""Script python qui va lancer la caméra py et permettre à mjpg-streamer de générer les flux et les images statiques
A indiquer dans le crontab en @reboot"""

import subprocess
from time import sleep
from configparser import ConfigParser

parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

cam_py_W = parser.get("camera", "cam_py_W")
cam_py_H = parser.get("camera", "cam_py_H")
cam_py_quality = parser.get("camera", "cam_py_quality")
cam_py_port = parser.get("camera", "cam_py_port")
cam_py_fps = parser.get("camera", "cam_py_fps")
mjpg_path = parser.get("paths", "mjpg")
delay_run=int(parser.get("frequences", "delay_run_Cam_py"))

sleep(delay_run)  #attente avant de lancer les commandes
command_py = "cd {} && export LD_LIBRARY_PATH=. && ./mjpg_streamer -o 'output_http.so -p {} -w ./www' -i 'input_raspicam.so -x {} -y {} - quality {} -fps {} '".format(mjpg_path, cam_py_port, cam_py_W, cam_py_H, cam_py_quality, cam_py_fps)
subprocess.run(command_py, shell=True)
```
