---
title: "Configuration.ini"
date: 2021-01-23T20:19:31+01:00
draft: false
---
```
;Fichier ini. A placer dans /etc/camera
;ini file, to set in /etc/camera

[locate]

;par défaut : le centre de la France selon l'IGN, Corse non comprise
;default : centre of France according IGN, Corse not included

longitude=2.430278
latitude=46.539722
altitude=326
zone=Europe/Paris


[hosts]

local=127.0.0.1

;ip locale Raspberry - port du serveur Django
;MODIFIER L'IP LOCALE DE LA RASPBERRY (raspIP) EN FONCTION DE VOTRE VALEUR
;local ip Raspberry - Django server port
;CHANGE THE LOCAL IP OF THE RASPBERRY (raspIP) ACCORDING TO YOUR VALUE

raspIP=<local IP Raspberry>

;port du serveur Django
;Django server port

django_port=8000

;proxy pour accès extérieur 
;proxy for outdoor internet access
proxy_1=Rp1
proxy_2=Rp2
proxy_py=Rpi


[mails]

;mail du site (celui avec lequel on crée un compte chez le fournisseur DynDNS)
;ce mail peut être le même que le mail personnel ; mais il vaut mieux en créer un
;VOUS DEVEZ RENSEIGNER LES DONNNEES DES DEUX MAILS AVEC VOS VALEURS
;site email (the one with which we create an account with the DynDNS provider)
;this email can be the same as the personal email; but it is better to create one
;YOU MUST FILL IN THE DATA OF BOTH EMAILS WITH YOUR VALUES

mail_site=<user1>@<provider1>

;mot de passe du mail_site
;password mail_site

mail_site_mdp=<password>

;mail personnel (celui auquel vont être envoyées diverses alertes et informations)
;personal email (the one to which various alerts and information will be sent)

mail_perso=<user2>@<provider2>

;port du smtp. Le port le plus usité est le 587, c'est donc celui par défaut
;si votre fournisseur d'adresse mail de mail_site a un autre port, le modifier
;en cas d'échec essayer dans l'ordre (après le 587) : 2525, puis 465
;smtp port. The most used port is 587, so it is the default one
;if your mail_site email address provider has another port, change it
;in case of failure try in order (after 587): 2525, then 465

smtp_port=587


[camera]
;ports sur lesquels les trois caméras vont être lues par mjpg-streamer
;ports on which the three cameras will be read by mjpg-streamer

cam_1_port=8081
cam_2_port=8082
cam_py_port=8084

;localisation des deux caméras USB (cam_1 et cam_2). Prendre les valeurs trouvées dans le fichier /dev/v4l/by-id en choisissant cells se terminant par -index0
;VOUS DEVEZ RENSEIGNER LES DONNNEES AVEC VOS VALEURS
;location of the two USB cameras (cam_1 and cam_2). Take the values ​​found in the / dev / v4l / by-id file by choosing cells ending in -index0
;YOU MUST FILL IN THE DATA WITH YOUR VALUES

cam_1_name=<value1>-video-index0
cam_2_name=<value2>-video-index0

;résolution des caméras USB
;USB cameras resolution

cam_1_resol=640x480
cam_2_resol=640x480

;résolutionde la pi-camera : WxH et qualité de l'image
;resolution of the pi-camera: WxH and picture quality

cam_py_W=640
cam_py_H=480
cam_py_quality=85 

;nombre d'images/seconde
;frames per second

cam_1_fps=5
cam_2_fps=5
cam_py_fps=5  


[paths]

;dossier de mjpg-streamer
;mjpg-streamer folder

mjpg=/home/pi/mjpg-streamer-experimental  

;chemin de home/utilisateur
;home/user path

home=/home/pi

;dossier principal
;main folder

folder=folder  

;dossier de l'environnement virtuel
;virtual environment folder

venv=folder_venv     

;nom du projet Django  
;Django project name

project=project 

;nom de l'application du projet 
;name of the project application

appli=camera

;dossier où sont stockées les photos 
;folder where photos are stored  

stock=/var/www/stock

;dossier des divers scripts
;various scripts folder

script=/home/pi/script  

;sous-dossier où vont être stockées les différentes images
;sub-folder where the different images will be stored

pathCamera_1=Camera_1
pathCamera_2=Camera_2
pathCamera_py=Camera_py

;nom de la base de données - nom de la sauvegarde de la base de données
;database name - name of the database backup

baseName=db.sqlite3
baseBackUp=back_up.sqlite3


[frequences]

;les fréquences historiques et nuit correspondent au nombre d'images qui seront présentées : si la valeur est N, il sera affiché une image sur N
;the historical (historique) and night (nuit) frequencies correspond to the number of images that will be presented: if the value is N, a frame out of N will be displayed

historique=4
nuit=3

;la capture est la fréquence de prise de vues en secondes ; la valeur est un entier compris entre 1 et 60 ; si N est égale à 1 il y a une prise de vue par seconde ; si N est égale à 60 il y a une prise de vue par minute
;capture is the shooting frequency in seconds; the value is an integer between 1 and 60; if N is equal to 1 there is one shot per second; if N is equal to 60 there is one shot per minute

capture=60 

;display_jour correspond au nombre de jours que l'on va visionner dans les vues historiques ; c'est un nombre flottant ; si égal à un on affiche les vues d'une journée ; si 2, celles de 2 jours...
;display_jour corresponds to the number of days that we will view in the historical views; it is a floating number; if equal to one, the views of a day are displayed; if 2, those of 2 days ...

display_jour=1

;temps d'attente pour lancer les scripts runCamera - si on les lance trop tôt, les caméras risquent de ne pas être montées avant le lancement du script - exprimé en secondes
;wait time to launch runCamera scripts - if started too early, cameras may not be mounted before the script starts - expressed in seconds

delay_run_Cam_1=75
delay_run_Cam_2=120
delay_run_Cam_py=50

;temps (en jours) pendant lequel on garde les fichiers photos
;tous les jours, on détruit les fichiers plus anciens que N jours
;doit être entier
;time (in days) during which the photo files are kept
;every day, we destroy files older than N days
;must be integer

delay_delete=2

;temps d'attente pour que la raspberry envoie un courriel après redémarrage (en secondes)
;wait time for the raspberry to send an email after restart (in seconds)

delay_send_mail_reboot=180
```
