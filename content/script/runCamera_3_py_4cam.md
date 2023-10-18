---
title: "RunCamera_1_4cam.py"
date: 2023-10-17T23:09:33+01:00
draft: false
---

```python
"""Script python qui va lancer la caméra supplémentaire et permettre à mjpg-streamer de générer les flux et les images statiques
A indiquer dans le crontab en @reboot"""

import subprocess
from time import sleep
from configparser import ConfigParser

parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

cam_3_name = parser.get("camera", "cam_3_name")
cam_3_port = parser.get("camera", "cam_3_port")
cam_3_resol = parser.get("camera", "cam_3_resol")
cam_3_fps = parser.get("camera", "cam_3_fps")
mjpg_path = parser.get("paths", "mjpg")
delay_run=int(parser.get("frequences", "delay_run_Cam_3"))

sleep(delay_run)  #attente avant de lancer les commandes
#command_cp = ["cp", f'{path_db}{baseName}', f'{path_db}/{baseBackUp}']
#command_1 = ["cd", f'{mjpg_path}', "&&", "export", f'LD_LIBRARY_PATH=.', "&&", f'./mjpg_streamer', "-i", 'input_uvc.so -r {} -fps {} -d /dev/v4l/by-id/{}' -o 'output_http.so -p {} -w {}/www']".format(mjpg_path,cam_1_resol, cam_1_fps, cam_1_name, cam_1_port, mjpg_path)
command_3 = "cd {} && export LD_LIBRARY_PATH=. && ./mjpg_streamer -i 'input_uvc.so -r {} -fps {} -d /dev/v4l/by-id/{}' -o 'output_http.so -p {} -w {}/www'".format(mjpg_path,cam_3_resol, cam_3_fps, cam_3_name, cam_3_port, mjpg_path)
subprocess.run(command_3, shell=True)
```
