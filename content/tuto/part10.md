---
title: "Tutoriel : Partie 10 - Mise en place de 2 Raspberry"
date: 2024-01-04T09:17:44+01:00
draft: false
---
## Position du problème
- La Raspberry peut être limitée en termes de capacités
- Soit parce que le nombre de caméras est élevé et que la Raspberry va peiner à traiter toutes les images
- Soit parce qu'on souhaite utiliser deux caméras pi et que la Raspberry ne peut en accueillir qu'une
- Nous appelons Raspberry Principale la Raspberry qui héberge le site Django
- Et Raspberry Secondaire la nouvelle Raspberry
## Schéma de la procédure
- Installer la Raspberry Secondaire et la caméra
- Créer les scripts sur cette Raspberry
- Créer un répertoire de stockage des photos sur la Raspberry Principale et créer la caméra dans la base de données
- Modifier le serveur Apache sur la Raspberry Principale
## Installer la Raspberry Secondaire
- Préparer la Raspberry : procédure de la [première partie du tutoriel]( {{< ref "part1#mise-en-route-de-la-raspberry" >}} )
- Mettre en place sur cette Raspberry `mjpg-streamer`
- C'est la même procédure que celle indiquée dans la [deuxième partie du tutoriel]( {{< ref "part2" >}} )
- On peut mettre en place un fichier de configuration sur cette Raspberry Secondaire
- Dans ce tutoriel, on simplifie en codant *en dur* les variables liées à la Raspberry Secondaire
- Installer la camera en suivant la procédure du [tutoriel]({{< ref "part2.md#installation-et-dénomination-des-caméras" >}})
## Créer les scripts sur la Raspberry Secondaire
### Créer différents dossiers
- Créer un dossier script placé dans /home/pi/
    ```sh
    mkdir ~/script
    ```
- Créer un dossier de stockage des images  
    ```sh
    sudo mkdir /var/www/stock /var/www/stock/Camera
    ``` 
- Changer le propriétaire de /var/www/stock
    ```sh
    sudo chown -R pi /var/www/stock
    ```
### Script de lancement de la camera
#### Créer le script en écriture
```sh
nano ~/script/runCamera.py
```
#### Écrire le contenu
```python
import subprocess
from time import sleep

"""Modifier les valeurs en fonction"""
mjpg_path = "/home/pi/mjpg-streamer-experimental"
cam_name = "xxxx-video-index0"
cam_port = "8088" 
cam_resol = "640x480"  
cam_fps = 5

delay_run = 60

sleep(delay_run)  #attente avant de lancer les commandes

command = "cd {} && export LD_LIBRARY_PATH=. && ./mjpg_streamer -i 'input_uvc.so -r {} -fps {} -d /dev/v4l/by-id/{}' -o 'output_http.so -p {} -w {}/www'".format(mjpg_path,cam_resol, cam_fps, cam_name, cam_port, mjpg_path)

subprocess.run(command, shell=True)
```
- Modifier les valeurs en fonction des paramètres choisis
#### Lancer le script au démareage
- Ouvrir le crontab
```sh
crontab -e
```
- Ajouter la commande
```sh
@reboot python3 /home/pi/script/runCamera.py
```
### Script d'envoi des images vers la Raspberry Principale
#### Principe
- Les images vont être stockées dans le dossier `/var/www/stock/Camera` de la deuxième caméra toutes les minutes
- Elles sont envoyées par le protocole `scp` sur la Raspberry principale
- Elles sont stockées dans un dossier `/var/www/stock/Camera_n` où `n` représente la n-ième caméra du système
#### Charger les bibliothèques nécessaires
- Ouvrir un terminal dans la Raspberry Secondaire : `Ctrl + Alt + T`
- Installer les deux bibliothèques nécessaires
    ```sh
    pip3 install paramiko
    pip3 install scp
    ```
#### Créer le script en écriture dans la Raspberry Secondaire
```sh
nano ~/script/stockAndSendImage.py
```
#### Écrire le contenu
```python
import paramiko
from scp import SCPClient
from datetime import datetime
from time import sleep
import subprocess

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

"""Modifier les valeurs en fonction"""
delay = 8   # délai en secondes entre la prise de la photo et son envoi par le protocole scp
# Les données concernant la Raspberry Principale
server = "192.168.1.50" # l'adresse IP locale de la Raspberry Principale qui porte le site Django
port = "22"  # le port usuel du ssh en local
user = "pi"  # si vous n'avez pas modifié le nom d'utilisateur de la Raspberry Principale
password = "le mot de passe de la Raspberry Principale" 
path_server = "/var/www/stock/Camera_8"   # modifier selon le lieu de stockage sur la Raspberry Principale

# Les données concernant la Raspberry Secondaire
sender = "127.0.0.1"   # peut aussi être remplacé par 192.168.1.xx ; représente l'ip locale de la Raspberry Secondaire
cam_port = "8088"   # le port donné à la caméra de la Raspberry Secondaire
path_sender = "/var/www/stock/Camera"   # le lieu de stockage défini au niveau de la Raspberry Secondaire

name = datetime.now().strftime("%d-%m_%H:%M:00")  # le nom de la photo du type 25-06_19:52:00 si la photo a été prise un 25 juin à 19h52

command = 'wget http://{}:{}/?action=snapshot -O {}/{}.jpg'.format(sender, cam_port, path_sender, name)
subprocess.run(command, shell=True)

sleep(delay)

ssh = createSSHClient(server, port, user, password)  # création du client ssh : la Raspberry Principale
scp = SCPClient(ssh.get_transport())
scp.put(f'{path_sender}/{name}.jpg',f'{path_server}')   # envoi de la photo en scp
scp.close()
print("closed / end")
```
#### Lancer le script toutes les minutes
- Ouvrir le crontab
```sh
crontab -e
```
- Ajouter la commande
```sh
* * * * * python3 /home/pi/script/stockAndSendImage.py
```
### Script de destruction périodique des photos stockées
- On procède comme cela a été fait pour la [Raspberry Principale]({{< ref "part3.md#ecrire-le-script-de-destruction-périodique-des-photos" >}})
- Créer et ouvrir en écriture le fichier suppressFiles<span></span>.py
    ```sh
    nano ~/script/suppressFiles.py
    ```
- Copier le code suivant
    ```python
    from subprocess import run

    path = "/var/www/stock/Camera"
    delay_delete = 2   # en jours : nombre de jours de stockage des photos

    command = ["find", f'{path}', "-mtime", f'+{str(delay_delete)}', "-delete"]
    run(command)
    ```
- Lancer le script tous les jours à 03H10 du matin (par exemple) dans le crontab
	- Ouvrir le cron en édition
    ```sh
    crontab -e
    ```  
    - Ajouter la ligne suivante
    ```sh
    10 03 * * * python3 /home/pi/script/suppressFiles.py
    ```

## Modifications au niveau de la Raspberry Principale
### Coder en dur ?
- Soit on apporte les modifications de variable au niveau du fichier `/etc/camera/configuration.ini`
- Soit on code en dur dans les différents fichiers
- Dans ce tutoriel, par simplification, on code en dur
### Créer un répertoire de stockage
- Se connecter en `ssh` à la Raspberry Principale
- Créer le dossier Camera-n (où n représente la n-ième caméra)
    ```sh
    mkdir /var/www/stock/Camera-n
    ``` 
- A priori, inutile d'être en `sudo` : `pi` a les droits sur le dossier /var/www/stock
### Modifier le fichier de suppression des images
- Ouvrir le fichier suppressFiles 
```sh
nano ~/script/suppressFiles.py
```
- Ajouter la commande de suppression des fichiers
```python
command_8 = ["find", f'{stock}/Camera-8', "-mtime", f'+{str(delay_delete)}', "-delete"]
```
- En modifiant, éventuellement, le nom de la commande et `Camera-8` par le nom du dossier où sont stockées les photos dans la Raspberry Principale
- Et lancer la commande en ajoutant
```python
run(command_8)
```
### Créer la caméra dans la base de données
- Procéder comme dans le tutoriel [Partie 8 - Créer la caméra]({{< ref "part8#créer-la-caméra-dans-la-base-de-données" >}})
- Ouvrir le `shell` en environnement virtuel
- Créer la caméra en lui donnant la valeur `Appareil(name="Cam_n)` (par exemple `Cam_8`)
- Quitter le `shell`
### Modifier le fichier getCamerasAndRegister.py
- Il faut que les images stockées dans `/var/www/stock` soient intégrées dans la base de données
- Dans cette configuration, on a deux caméras au niveau de la raspberry secondaire : Camera_5 et Camera_ir (une pi-camera)
- Ajouter avant la boucle `while True`

```python
# Ajout des caméras de la 2ème raspberry
pathCamera_5 = "Camera_5"
pathCamera_ir = "Camera_ir"
```
- Ajouter dans la boucle `while True` avant `conn.commit()`

```python
# Ajout des caméras de la 2ème raspberry
c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '5', ?, ?)".format(appli), (date, name, pathCamera_5))
c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '6', ?, ?)".format(appli), (date, name, pathCamera_ir))
```
- Tout ceci si on a nommé les dossiers de stockage `Camera_5` et `Camera_ir` 
- Et si on a créé deux caméras dans le shell

- Le nouveau fichier `getCamerasAndRegister.py` est visible dans la partie [script]({{< ref "/script/getCamerasAndRegister_py_2Raspberry.md" >}})

### Modifier les fichiers urls.py et views.py
- Suivre les indications données dans le tutoriel [Partie 8 - Fichiers urls et views]({{< ref "part8.md#modifier-les-fichiers-urls-et-views-de-django" >}})
- Modifier `urls.py` en ajoutant le path pour le streaming, par exemple `stream_8`
- Dans `views.py`, modifier les fonctions *ad hoc*
- Y ajouter la fonction de streaming (par exemple, si la caméra est la 8)
```python
def stream_8(request):
    stream = ["/Rp8?action=stream"]
    context = {
        'stream': stream,
    }
    return render(request, "{}/stream_8.html".format(appli), context)
```
### Modifier les fichiers html
- Suivre les indications données dans le tutoriel [Partie 8 - Fichiers html]({{< ref "part8.md#modifier-les-fichiers-html-templates" >}})
### Modifier le fichier de configuration apache2
- Suivre les indications données dans le tutoriel [Partie 8 - Fichier de configuaration apache]({{< ref "part8.md#modifier-le-fichier-de-configuration-apache2-du-site" >}})
- Au niveau des `proxyPass`, il convient de modifier l'adresse `ip` en y affectant l'adresse de la Raspberry Secondaire
- Ajouter dans le fichier `/etc/apache2/sites-available/project-camera.conf`, aux endroits ad hoc des lignes du style 
```sh
ProxyPass /Rp8 http://<localIP RaspberrySecondaire>:8088/
ProxyPassReverse /Rp8 http://<localIP RaspberrySecondaire>:8088/
```
- Si l'**adresse de la Raspberry Secondaire** est `192.168.1.36`, par exemple, cela donnera
```sh
ProxyPass /Rp8 http://192.168.1.36:8088/
ProxyPassReverse /Rp8 http://192.168.1.36:8088/
```
- Il faut modifier ces lignes au niveau dc chaque `VirtualHost`, c'est à dire le `443` et le `88`
- Ne pas oublier de relancer `apache2`
```sh
sudo systemctl restart apache2
```