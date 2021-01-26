---
title: "Configuration.ini"
date: 2021-01-23T20:19:31+01:00
draft: false
---
```
; Fichier ini. A placer dans /etc/camera

[locate]
;par défaut : le centre de la France selon l'IGN, Corse non comprise : 
;longitude = 2.430278
;latitude = 46.539722
;altitude = 326
longitude=2.430278
latitude=46.539722
altitude=326
zone=Europe/Paris

; ip locale du serveur - port du serveur Django
; proxy pour accès extérieur 
; MODIFIER L'IP LOCALE DE LA RASPBERRY EN FONCTION DE VOTRE VALEUR
[hosts]
local=127.0.0.1
raspIP=192.168.1.49
django_port=8000
proxy_1=Rp1
proxy_2=Rp2
proxy_py=Rpi

; boîtes courriels : mail du site et son mot de passe, mail personnel et informations utiles pour le module smtplib
[mails]
;mail du site (celui avec lequel on crée un compte chez le fournisseur DynDNS)
;ce mail peut être le même que le mail personnel ; mais il vaut mieux en créer un
;notamment pour éviter que le mot de passe de votre mail personnel ne soit en clair sur la raspberry
;VOUS DEVEZ RENSEIGNER LES DONNNEES DES MAILS AVEC VOS VALEURS
mail_site=xxxxx@laposte.net
;mot de passe du mail du site
mail_site_mdp=zzzz-xxxx-yyyy-11111
;mail personnel (celui auquel vont être envoyées diverses alertes et informations)
mail_perso=yyyyy@gmail.com
;port du smtp. Le port le plus usité est le 587, c'est donc celui par défaut
;si votre fournisseur d'adresse mail de mail_site a un autre port, le modifier
;en cas d'échec essayer dans l'ordre (après le 587) : 2525, puis 465
smtp_port=587

;caractéristiques des caméras
[camera]
;ports sur lesquels les trois caméras vont être lues par mjpg-streamer
cam_1_port=8081
cam_2_port=8082
cam_py_port=8084

;localisation des deux caméras USB (cam_1 et cam_2). Prendre les valeurs trouvées dans le fichier /dev/v4l/by-id en choisissant cells se terminant par -index0
cam_1_name=uusb-AVEO_Technology_Corp._USB2.0_Camera-video-index0
cam_2_name=usb-046d_08ce_51B7BEC2-video-index0

;résolution des caméras USB
cam_1_resol=640x480
cam_2_resol=640x480
;résolutionde la cam py : WxH et autres paramètres
cam_py_W=640
cam_py_H=480
;qualité de l'image, de 0 à 100
cam_py_quality=85 
;nombre d'images/seconde
cam_1_fps=5
cam_2_fps=5
cam_py_fps=5  

;variables pour les chemins des fichiers. Nommer folder/project/application
[paths]
; dossier où se trouve mjpg-streamer
mjpg=/home/pi/mjpg-streamer-experimental   
;chemin de home/utilisateur
home=/home/pi
;dossier général
folder=folder  
;nom de l'environnement virtuel
venv=folder_venv     
;nom du projet Django  
project=project 
;nom de l'application du projet         
appli=camera
;dossier où sont stockées les photos          
stock=/var/www/stock
;dossier de sauvegarde des photos avant suppression 
stock_save=/home/pi/stock_backup
;dossier où sont les divers scripts
script=/home/pi/script  

; sous-dossier où vont être stockées les différentes images
pathCamera_1=Camera_1
pathCamera_2=Camera_2
pathCamera_py=Camera_py

;nom de la base de données ; nom de la sauvegarde de la base de données
baseName=db.sqlite3
baseBackUp=back_up.sqlite3

; les fréquences historiques et nuit correspondent au nombre d'images qui seront présentées : si la valeur est N, il sera affiché une valeur sur N
; la capture est la fréquence de prise de vues en secondes ; la valeur est un entier compris entre 1 et 60 ; si N est égale à 1 il y a une prise de vue par seconde ; si N est égale à 60 il y a une prise de vue par minute
; display_jour correspond au nombre de jours que l'on va visionner dans les vues historiques ; c'est un nombre flottant ; si égal à un on affiche les vues d'une journée ; si 2, celles de 2 jours...
[frequences]
historique=4
nuit=3
capture=60 
display_jour=1
;temps d'attente pour lancer les scripts runCamera - si on les lance trop tôt, les caméras risquent de ne pas être montées avant le lancement du script - nombre de secondes
delay_run_Cam_1=75
delay_run_Cam_2=120
delay_run_Cam_py=50

;temps (en jours) pendant lequel on garde les fichiers photos
;tous les jours, on détruit les fichiers plus anciens que N jours
;doit être entier
delay_delete=2

;temps d'attente pour que la raspberry envoie un courriel après redémarrage (en secondes)
delay_send_mail_reboot=180
```
