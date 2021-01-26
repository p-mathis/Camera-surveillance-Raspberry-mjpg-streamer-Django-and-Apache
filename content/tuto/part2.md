---
title: "Tutoriel : Partie 2 - Installation de mjpg-streamer"
date: 2021-01-23T22:57:16+01:00
draft: false
---

## A faire
- Installer mjpg-streamer
- Désigner les caméras USB de manière unique
- Scripts de lancement des caméras
## Installation de mjpg-streamer
- Il existe deux façons d’installer mjpg-streamer :
  - en utilisant la commande snap
  - en passant par la page [github](https://github.com/jacksonliam/mjpg-streamer) de Jackson Liam  
- La méthode snap est la plus simple, mais on ne peut pas l'utiliser ici car elle n'installe pas le module input_raspicam qui gère la pi-caméra.
## Installer avec github
- Cloner le dépôt git
    ```sh
    git clone https://github.com/jacksonliam/mjpg-streamer.git
    ```
- Déplacer le dossier de `~/mjpg-streamer` vers `~/`
  - le dossier mjpg-streamer-experimental s'est copié dans un dossier parent mjpg-streamer
  - le déplacer vers /home/pi
    ```sh
    mv ~/mjpg-streamer/mjpg-streamer-experimental ~/
    ```
- Suppression du dossier mjpg-streamer (en sudo car contient un fichier protégé)
    ```sh
    sudo rm -R mjpg-streamer
    ```
- Installation des dépendances :
    ```sh
    sudo apt install cmake libjpeg8-dev -y
    ```
Si la question `souhaitez-vous continuer` est posée, taper `O`  
- A priori les dépendances gcc et g++ sont déjà installées. Sinon les installer
    ```
    sudo apt install gcc g++
    ```
- Compilation
    ```sh
    cd ~/mjpg-streamer-experimental
    make
    sudo make install
    ```
## Installation et dénomination des caméras
*Remarque : la pi caméra a été malencontreusement dénommée au départ camera_py, avec un y et non un i. Modifier a posteriori cette coquille serait source d’erreur, aussi le y a été laissé dans les dénominations des dossiers, fichiers et variables.*
- Brancher la pi-camera si cela n'est pas déjà fait 
  - ***Attention : la raspberry doit être éteinte pour brancher la pi-camera***
  - Consulter un tutoriel dédié. Par exemple celui de [projects.raspberry](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/1)
- Brancher les deux caméras USB si cela n’est pas déjà fait.
- Dans le répertoire `/dev/v4l/by-id` répertorier l’identifiant des caméras USB
    ```sh
    ls /dev/v4l/by-id
    ```
- La commande renvoie des lignes du style : 
    ```sh
    <valeur1>-video-index0
    <valeur1>-video-index1
    <valeur2>-video-index0
    <valeur2>-video-index1 
    ```
- Dans un deuxième terminal connecté en ssh ouvrir le fichier de configuration
    ```sh
    sudo nano /etc/camera/configuration.ini
    ```
- Dans la section `[camera]` chercher les clés `cam_1_name` et `cam_2_name`
- Remplacer, par un copier/coller, les valeurs mises par défaut par les valeurs `<valeur1>-video-index0` et `<valeur2>-video-index0` lues dans l’autre terminal.
- Ceci permet d’identifier de manière unique les flux vidéos dans les scripts de lancement de mjpg-streamer.
## Modification des paramètres des caméras
Si vous le souhaitez vous pouvez modifier les paramètres des caméras dans le fichier configuration.ini : ports de sortie pour mjpg-streamer, résolution etc.  
Sinon, laissez les valeurs par défaut.  
En fonction de l’ancienneté et de la qualité de vos caméras, certains paramètres seront à ajuster : la résolution, le nombre d’images par seconde (fps) notamment.
## Scripts de lancement des caméras
- Créer un dossier script placé dans /home/pi/
    ```sh
    mkdir ~/script
    ```
Vous pouvez nommer ce dossier autrement, mais dans ce cas vous devrez modifier la valeur par défaut du dossier dans le fichier configuration.ini (section `[paths]` clé `script`).  
C'est dans ce dossier que seront placés différents scripts.
- Créer runCamera_1<span0></span>.py
  - Créer en écriture le fichier
    ```sh
    nano ~/script/runCamera_1.py
    ```
  - Copier le contenu du fichier runCamera_1<span></span>.py disponible en cliquant [ici]({{< ref "/script/runCamera_1_py.md" >}} "runCamera_1")
  - Coller ce contenu dans la fenêtre de l'éditeur nano
  - Enregsitrer et fermer
- Créer runCamera_2<span></span>.py de la même manière (pour copier le fichier : cliquer [ici]({{< ref "/script/runCamera_2_py.md" >}} "runCamera_2"))
- Créer runCamera_py<span></span>.py de la même manière (pour copier le fichier : cliquer [ici]({{< ref "/script/runCamera_py_py.md" >}} "runCamera_py"))
- Une variable `delay_run` permet de différer le lancement du script pour éviter que le script ne tourne avant que les caméras n'aient été installées par la Raspberry. Il est possible de modifier ces variables dans le fichier de configuration (section `[frequences]`, clés `delay_run_Cam_1`, `delay_run_Cam_2`, `delay_run_Cam_py`)
### Tester les caméras
On peut tester les caméras, par exemple la caméra 1  
- Lancer le script runCamera_1.py
    ```sh
    python3 ~/script/runCamera_1.py
    ```
*La commande est python3 et non python ! Effectivement la version par défaut de raspbian est python2.*
- Attendre le délai de lancement du script (!) et une fois le script lancé :
- Dans la barre d'adresse d'un navigateur taper : `<local IP Raspberry>:8081/` (par exemple `192.168.1.49:8081/`).
- Vous devez obtenir une page web semblable à celle-ci  
{{< figure src="/media/mjpg_accueil.png">}}
- Visionner le flux en cliquant sur l'onglet `Stream`
- Les deux autres caméras sont visualisées en adaptant le port : 8082 et 8084 (modifier les ports si ils ont été changés dans le fichier de configuration).
## Lancer les caméras et les flux au démarrage
Pour lancer automatiquement les caméras et les flux au démarrage de la raspberry, il faut écrire les commandes dans le crontab.  
- Ouvrir le crontab
    ```sh
    crontab -e
    ```
- A la première utilisation du crontab, on vous demande de choisir l’éditeur. Taper 1 si vous souhaitez utiliser nano.  
- A la fin du fichier crontab ajouter les trois lignes suivantes :
    ```sh
    @reboot python3 /home/pi/script/runCamera_1.py
    @reboot python3 /home/pi/script/runCamera_2.py
    @reboot python3 /home/pi/script/runCamera_py.py
    ```
- Ici aussi, la commande doit être python3 et non pas python. Bien sûr sauvegarder et quitter.
- `@reboot` signifie que la commande sera lancée à chaque démarrage de la raspberry.
- En cas d’absence de flux de l’une des caméras, rebouter le système en lançant la commande : 
    ```sh
    sudo reboot
    ```
## A ce stade - Prochaine étape
### A ce stade
- 3 caméras ont été installées
- Les flux des caméras peuvent être consultés sur un appareil du réseau local en tapant dans la fenêtre d'un navigateur web `<local IP Raspberry>:<port camera>/` (par exemple : `192.168.1.49:8082/`)
### Prochaine étape
- Installer le cadre de développement (framework) Django
- Utiliser Django pour créer un site web avec des requêtes répondant au cahier des charges du projet
