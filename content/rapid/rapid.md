---
title: "Guide Rapide"
date: 2021-01-23T19:44:10+01:00
draft: false
---

## Préalable
Raspbian est installé sur la Raspberry. Celle-ci est accessible par SSH depuis un ordinateur à partir duquel sont lancées toutes les commandes.  
La Raspberry a une IP locale fixe.  
La pi-caméra et les deux caméras USB sont branchées.
## Installation de logiciels et de dépendances
- mise à jour (si raspbian est d'installation ancienne)  

      sudo apt update && sudo apt upgrade -y

- dépendances pour mjpg-streamer

      sudo apt install cmake libjpeg8-dev -y

- apache2 et ses dépendances

      sudo apt install apache2 apache2-dev

- snapd (pour une installation simplifiée de certbot)  

      sudo apt install snapd

- rebouter le système pour installer snap  

      sudo reboot

- installer core une fois le système rebouté  

      sudo apt install core

- installer certbot  

      sudo snap install --classic certbot

## Installation d'un fichier de configuration

    sudo mkdir /etc/camera
    sudo nano /etc/camera/configuration.ini

- Copier/coller dans la fenêtre le contenu du fichier `configuration.ini` disponible [ici]({{< ref "/script/configuration_ini.md" >}} "configuration_ini").
- Modifier ou renseigner les valeurs suivantes :
  - `[locate]` : renseigner longitude, latitude, altitude et zone en fonction de vos valeurs
  - `[hosts]` : renseigner raspIP en fonction de l'IP locale de votre Raspberry
  - `[mails]` : renseigner les différentes adresses mail et le mot de passe
  - `[camera]` : cam_1_name et cam_2_name seront renseignés plus [loin](#dénomination-des-caméras) ; les autres valeurs peuvent être inchangées ou modifiées à votre convenance.  
  - `[paths]` et `[frequences]` : ne rien modifier *a priori*
## Installation de mjpg-streamer et des caméras
### Installer mjpg-streamer
- Cloner le dépôt git

      git clone https://github.com/jacksonliam/mjpg-streamer.git

- Déplacer mjpg-streamer-experimental dans /home/pi

      mv ~/mjpg-streamer/mjpg-streamer-experimental ~/

- Compilation
    ```sh
    cd ~/mjpg-streamer-experimental
    make
    sudo make install
    ```

### Dénomination des caméras
- Dans le répertoire /dev/v4l/by-id répertorier l’identifiant des caméras

      ls /dev/v4l/by-id

- La commande retourne 4 lignes du style :
    ```sh
    <valeur1>-video-index0
    <valeur1>-video-index1
    <valeur2>-video-index0
    <valeur2>-video-index1 
    ```
- Dans le fichier de configuration remplacer les valeurs des clés `cam_1_name` et `cam_2_name` par les valeurs `<valeur1>-video-index0` et `<valeur2>-video-index0`
## Installation de Django
### Création d'un environnement virtuel
- Création du dossier folder et de l'environnement virtuel
    ```sh
    mkdir ~/folder
    cd ~/folder
    python3 -m venv folder_venv
    ```
- Pour activer l'environnement virtuel

      source ~/folder/folder_venv/bin/activate

- L'invite de commande ne sera plus du style `pi@Foo:~ $` mais `(folder_venv) pi@Foo:~ $`
- Pour désactiver l'environnement virtuel

      deactivate

- ***Dorénavant, lorsque les commandes seront tapées dans l'environnement virtuel, elles seront précédées du symbole : (venv)***
### Installation de Django et de modules complémentaires
- Installer Django en environnement virtuel

      (venv) python -m pip install Django

- Vérifier l'installation et la version

      (venv) python -m django --version

qui doit renvoyer une sortie du type :  3.1.4 (en fonction de la version)
- Installer le module suntimes

      (venv) pip install suntimes

- Au besoin installer les dépendances de suntimes
    ```sh
    (venv) pip install jdcal
    (venv) pip install tzlocal
    ```
### Création du projet et de l'application
#### Création du projet project et de l'application camera
```sh
(venv) cd ~/folder
(venv) django-admin startproject project
(venv) cd ~/folder/project
(venv) python manage.py startapp camera
```
#### Structure de l'application camera
L'application camera va comporter huit vues :
- accueil : la page d’accueil du site
- historique : page présentant des photos prises à intervalle régulier par les trois caméras, sur une durée déterminée (par exemple, toutes les 5 minutes sur les 24 dernières heures)
- parHeure : pages avec pagination présentant toutes les photos prises sur une durée déterminée (par exemple, toutes les minutes sur les 24 dernières heures)
- nuit : page présentant des photos prises à intervalle régulier par la caméra nocturne du coucher du soleil au lever du soleil le lendemain
- stream_1 : flux vidéo en direct de la première caméra
- stream_2: flux vidéo en direct de la deuxième caméra
- stream_py : flux vidéo en direct de la pi-caméra
- stream_AllCam : flux vidéo en direct des trois caméras
### Réglages du fichier settings<span></span>.py
- Ouvrir le fichier `settings.py`

      nano ~/folder/project/project/settings.py

- ALLOWED_HOSTS : ajouter l'IP locale de la Raspberry

      ALLOWED_HOSTS = ['<local IP raspberry>']

- INSTALLED_APPS : ajouter `camera.apps.CameraConfig` dans la liste existante
    ```python
    INSTALLED_APPS = [
      'camera.apps.CameraConfig', 
      'django.contrib.admin', 
      'django.contrib.auth', 
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles', 
      ]
    ```
- DATABASES : ajouter votre time-zone
    ```python
    DATABASES = {  
      'default': {  
      'ENGINE': 'django.db.backends.sqlite3',  
      'NAME': BASE_DIR / 'db.sqlite3',  
      'TIME_ZONE': 'Europe/Paris'  
      }  
      }  
    ```
- LANGUAGE_CODE et TIME_ZONE : adapter la langue et la time-zone
    ```python
    LANGUAGE_CODE ='fr'
    TIME_ZONE = 'Europe/Paris'
    ```
### Créer les modèles de l'application
- Ouvrir le fichier `models.py`

      nano ~/folder/project/camera/models.py

- Remplacer son contenu par celui du fichier `models.py` disponible [ici]({{< ref "/script/models_py.md" >}} "models.py").
- Prendre en compte les modifications
    ```sh
    (venv) python ~/folder/project/manage.py makemigrations
    (venv) python ~/folder/project/manage.py migrate
    ```
- Créer les trois caméras
    ```sh
    (venv) python ~/folder/project/manage.py shell
    >>> from camera.models import Appareil 
    >>> c = Appareil(name="Cam_1")
    >>> c.save()
    >>> c = Appareil(name="Cam_2")
    >>> c.save()
    >>> c = Appareil(name="Cam_py")
    >>> c.save()
    ```
- Vérifier les enregistrements
    ```sh
    >>> Appareil.objects.all()
    <QuerySet [<Appareil: Cam_1>, <Appareil: Cam_2>, <Appareil: Cam_py>]>
    ```
- Quitter le shell : `Ctrl+D`
### Modifier le fichier urls<span></span>.py de ~/folder/project/project
- Ouvrir le fichier
    ```sh
      nano ~/folder/project/project/urls.py
    ```
- modifier la ligne d'import et la ligne urlpatterns de la manière suivante
    ```python
      from django.contrib import admin
      from django.urls import path, include

      urlpatterns = [
          path('camera/', include('camera.urls')),
          path('admin/', admin.site.urls),
      ]
    ```
### Créer un fichier urls<span></span>.py dans ~/folder/project/camera
- Créer et ouvrir le fichier en écriture

      nano ~/folder/project/camera/urls.py

- Coller/copier dans ce fichier le contenu du fichier `urls_camera.py` disponible [ici]({{< ref "/script/urls_py_camera.md" >}} "urls camera").
### Modifier le fichier ~folder/project/camera/views<span></span>.py
- Ouvrir le fichier  

      nano ~/folder/project/camera/views.py

- Effacer son contenu et copier/coller le contenu du fichier `views.py` disponible [ici]({{< ref "/script/views_py_V2.md" >}} "views.py V2").
### Créer les fichier css et un fichier logo
- Création des dossiers css et logo
    ```sh
    cd ~/folder/project/camera
    mkdir static static/camera static/camera/css static/camera/logo
    ```
- Créer et écrire le fichier general.css

      nano ~/folder/project/camera/static/camera/css/general.css

Copier/coller dans ce fichier le contenu du fichier `general.css` disponible [ici]({{< ref "/script/general_css.md" >}} "general.css").
- Procéder de même pour les autres fichiers css :
  - `bouton.css` dont le contenu est disponible [ici]({{< ref "/script/bouton_css.md" >}} "bouton.css")
  - `menu.css` dont le contenu est disponible [ici]({{< ref "/script/menu_css.md" >}} "menu.css")
  - `disposition.css` dont le contenu est disponible [ici]({{< ref "/script/disposition_css.md" >}} "menu.css")
  - `header_footer.css` dont le contenu est disponible [ici]({{< ref "/script/header_footer_css.md" >}} "menu.css")
  - `pagination.css` dont le contenu est disponible [ici]({{< ref "/script/pagination_css.md" >}} "pagination.css")
- Logo favicon  
  - Charger sur la Raspberry une image au format png d'environ 40x40 pixels
  - Nommer l'image `logo.png`
  - Déplacer l'image dans le dossier `~/folder/project/camera/static/camera/logo`
### Créer les fichiers html (templates)
- Création du dossier templates
    ```sh
    cd ~/folder/project/camera
    mkdir templates templates/camera
    ```
- Créer et écrire le fichier `base.html`

      nano ~/folder/project/camera/templates/camera/base.html

Copier/coller dans ce fichier le contenu du fichier `base.html` disponible [ici]({{< ref "/script/base_html.md" >}} "base.html").
- Procéder de même pour les autres fichiers html :
    - `accueil.html` dont le contenu est disponible [ici]({{< ref "/script/accueil_html.md" >}} "accueil.html")
    - `historique.html` dont le contenu est disponible [ici]({{< ref "/script/historique_html.md" >}} "historique.html")
    - `nuit.html` dont le contenu est disponible [ici]({{< ref "/script/nuit_html.md" >}} "nuit.html")
    - `parHeure.html` dont le contenu est disponible [ici]({{< ref "/script/parHeure_html.md" >}} "parHeure.html")
    - `stream_1.html` dont le contenu est disponible [ici]({{< ref "/script/stream_1_html.md" >}} "stream_1.html")
    - `stream_2.html` dont le contenu est disponible [ici]({{< ref "/script/stream_2_html.md" >}} "stream_2.html")
    - `stream_py.html` dont le contenu est disponible [ici]({{< ref "/script/stream_py_html.md" >}} "stream_py.html")
    - `stream_AllCam.html` dont le contenu est disponible [ici]({{< ref "/script/stream_AllCam_html.md" >}} "stream_AllCam.html")

## Nom de domaine - DynDNS - Modifications sur la box
### Obtenir un nom de domain chez No-IP
- Aller sur le site de [No-Ip](https://www.noip.com/)  
- Créer son site avec obtention du nom de domaine en suivant les instructions
### Modifications sur la box
Quelques modifications sont à apporter au niveau de la box. La marche à suivre décrit ci-dessous concerne une livebox Orange ; les proccédures sont similaires chez les autres opérateurs.
- Créer une règle `NAT/PAT` pour la raspberry sur les ports internes et externes 80
- Créer une règle `NAT/PAT` pour la raspberry sur les ports internes et externes 443
- Dans le service `DynDNS` attribuer le nom de domaine obtenu chez NoIP, renseigner l'adresse email et le mot de passe NoIP
## Paramétrages de Apache et de l'interface wsgi
### Sécurisation minimale du serveur apache
- Suivre les instructions de la page [wiki.debian](https://wiki.debian-fr.xyz/S%C3%A9curiser_Apache2#Limiter_les_informations_visibles)
- Ouvrir en écriture le fichier security.conf
    ```sh
    sudo nano /etc/apache2/conf-available/security.conf
    ```
- Modifier le fichier comme suit
  - modifier `ServerTokens Prod` (et non OS)  
  - modifier `ServerSignature Off` (et non On)  
  - laisser `TraceEnable Off`  
  - décommenter `Header set X-Content-Type-Options: "nosniff"`  
  - décommenter `Header set X-Frame-Options: "sameorigin"` 
- Modifier la page d'accueil Apache en la supprimant et en la remplaçant par une nouvelle
    ```sh
    sudo rm /var/www/html/index.html
    sudo nano /var/www/html/index.html
    ```
- Copier, par exemple, le script suivant dans cette nouvelle page
    ```html
    <html>
    PAGE INACCESSIBLE
    </html>
    ```
- Créer une page erreur 404

      sudo nano /var/www/html/missing.html

- Copier, par exemple, le script suivant dans cette nouvelle page
    ```html
    <html>
    DOCUMENT INEXISTANT<br>
    MISSING DOCUMENT
    </html>
    ```
- Modifier /etc/apache2/conf-available/localized-error-pages.conf  

      sudo nano /etc/apache2/conf-available/localized-error-pages.conf

- Et décommenter la ligne `ErrorDocument 404 /missing.html`
### Installation du module mod_wsgi
- Installer le module dans l'environnement virtuel

      (venv) pip install mod_wsgi

- Se placer dans le répertoire des packages python de l'environnement virtuel

      (venv) cd /home/pi/folder/folder_venv/lib/python3.7/site-packages

  (Modifier la commande en fonction de la version python de l'environnement virtuel)
- Lancer la commande suivante depuis ce répertoire 

      (venv) mod_wsgi-express module-config

- On obtient une sortie de ce type
    ```sh
    LoadModule wsgi_module "/home/pi/folder/folder_venv/lib/python3.7/site-packages/mod_wsgi/server/mod_wsgi-py37.cpython-37m-arm-linux-gnueabihf.so"
    WSGIPythonHome "/home/pi/folder/folder_venv"
    ```
- Créer un fichier wsgi.load dans /etc/apache2/mods-available

      sudo nano /etc/apache2/mods-available/wsgi.load

- Dans ce fichier coller les deux lignes récupérées précédemment
### Création des répertoires de stockage des photos
```sh
sudo mkdir /var/www/stock
cd /var/www/stock
sudo mkdir Camera_1 Camera_2 Camera_py
```
### Donner les droits à www-data et à l'utilisateur pi
- Créer un groupe composé de pi et www-data, appelé varwwwusers  
    ```sh
    sudo addgroup varwwwusers
    sudo adduser pi varwwwusers
    sudo adduser www-data varwwwusers
    ```
- Changer le propriétaire et les droits du dossier /var/www/stock

      sudo chown -R pi:varwwwusers /var/www/stock
      chmod -R 750 /var/www/stock

- Modifier le propriétaire et les droits de db.sqlite3
    ```sh
    sudo chown pi:www-data ~/folder/project/db.sqlite3
    sudo chmod 770 ~/folder/project/db.sqlite3
    ```
### Copier les fichiers statiques de Django vers /var/www/stock
```sh
cp -r ~/folder/project/camera/static/camera /var/www/stock
```
### Modifier le fichier settings<span></span>.py
- Ouvrir le fichier settings.py

      nano ~/folder/project/project/settings.py

- Mettre la valeur `DEBUG` à `False`

      DEBUG = False

- Masquer la clé de sécurité
  - Copier la valeur de `SECRET_KEY` 
  - Créer et ouvrir en écriture /etc/camera/secret_key.txt  

        sudo nano /etc/camera/secret_key.txt

  - Coller la valeur de `SECRET_KEY` dans ce fichier
- Remplacer la ligne `SECRET_KEY = '<votre SECRET_KEY>'` par
    ```python
      with open(‘/etc/camera/secret_key.txt’) as f:
        SECRET_KEY = f.read().strip()
  ```
- STATICFILES_DIRS : ajouter en fin du fichier `settings.py`
    ```python
    STATICFILES_DIRS = [  
    BASE_DIR / "/home/pi/folder/project/camera/static",  
      "/var/www/stock"  
      ] 

### Restreindre l'accès au site
- Créer le fichier .htaccess dans /etc/apache2

      sudo touch /etc/apache2/.htpasswd

-Créer un utilisateur, par exemple foo :

      sudo htpasswd /etc/apache2/.htpasswd foo

- A l’invite de commande 'New password' rentrer un mot de passe
- A l’invite de commande 'Re-type new password' rentrer à nouveau le mot de passe
- Le message " Adding password for user foo "  s’affiche.
- Créer autant d’utilisateurs que nécessaire en procédant de la même manière.
### Obtenir un certificat Certbot de Let's Encrypt
- Lancer la commande  

      sudo certbot certonly --apache --rsa-key-size 4096

- Répondre aux invites de commandes
### Créer le fichier de configuration project-camera.conf
- Créer et ouvrir le fichie en écriture

      sudo nano /etc/apache2/sites-available/project-camera.conf

- Coller/copier le contenu du fichier `project-camera.conf` disponible [ici]({{< ref "/script/project-camera_conf_V5.md" >}} "project-camera_V5.html").
- Renseigner le nom de son site partout où nécessaire
- Renseigner l'adresse IP locale de la raspberry partout où nécessaire
### Activer les différents modules de apache
- Activation des modules
    ```sh
    sudo a2enmod headers
    sudo a2enmod wsgi
    sudo a2enmod proxy_http
    sudo a2enmod ssl 
    sudo a2enmod rewrite
    ```
- Activation du site 

      sudo a2ensite project-camera

- Redémarrer apache2

      sudo systemctl restart apache2

### Accès au site
- Depuis l'extérieur du réseau, le site est accessible à l'adresse : \<nom du site\>/camera
- Depuis le réseau local, le site est accessible à l'adresse : \<adresse Ip locale\>:54321/camera
## Scripts de gestion
### Créer le dossier ~/script
```sh
mkdir ~/script
```
### Scripts de lancement des caméras
- Créer et écrire le fichier runCamera_1.py

      nano ~/script/runCamera_1.py

Et coller dans la fenêtre le contenu du fichier runCamera_1.py disponible [ici]({{< ref "/script/runCamera_1_py.md" >}} "runCamera_1")
- Faire de même pour les deux autres caméras en créant les fichiers et en copiant/collant le contenu des fichiers `runCamera_2.py` disponible [ici]({{< ref "/script/runCamera_2_py.md" >}} "runCamera_1") et `runCamera_py.py` disponible [ici]({{< ref "/script/runCamera_py_py.md" >}} "runCamera_1")
- Les scripts sont lancés après un délai d'attente paramétrable dans le fichier de configuration.
### Ecrire le script de capture et de stockage des photos
- Créer et ouvrir en écriture le fichier

      nano ~/script/getCamerasAndRegister.py

- Copier/coller dans la fenêtre le contenu du fichier `getCamerasAndRegister.py` disponible [ici]({{< ref "/script/getCamerasAndRegister_py.md" >}} "getCamerasAndRegister.py").
### Ecrire le script de destruction périodique des fichiers
- Créer et ouvrir en écriture le fichier

      nano ~/script/suppressFiles.py

- Copier/coller dans la fenêtre le contenu du fichier `suppressFiles.py` disponible [ici]({{< ref "/script/suppressFiles_py.md" >}} "suppressFiles.py").
### Mise à jour régulière du système
- Créer et ouvrir le fichier en écriture  
	`nano ~/script/updateAndUpgradeAuto.sh`  
- Ecrire le script en ajoutant les deux lignes
    ```sh
    #!bin/bash  
    sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y
### Etre informé par courriel des redémarrages de la raspberry
- Créer et ouvrir le script en écriture
    ```sh
    nano ~/script/mail_reboot.py
    ```
- Copier/coller le contenu du fichier `mail_reboot.py` disponible [ici]({{< ref "/script/mail_reboot_py.md" >}} "mail_reboot.py")    ```
## Contrôle de l'IP et envoi d'un mail en cas de changement
- Si une IP statique (fixe) n'est pas assujettie à la box, il faut être informé des changements d'IP.
- Créer et ouvrir en écriture le fichier ~/currentIP.txt  
    ```sh
    nano ~/currentIP.txt
    ```
- Ecrire la ligne suivante  
    ```sh
    {"ip": " ", "date": " "}
    ```
    *Si vous n'écrivez rien dans le fichier, lorsque le script se lancera il soulèvera une erreur.*
- Créer et ouvrir en écriture le fichier `~/script/ipcheck.py`  
    ```sh
    nano ~/script/ipcheck.py  
    ```
- Copier/coller le contenu du fichier `ipcheck.py` disponible [ici]({{< ref "/script/ipcheck_py.md" >}} "ipcheck.py")
### Lancement des différents scripts dans le cron
- Éditer le crontab
    ```sh
    crontab -e
    ```
- Copier dans le crontab les lignes suivantes
    ```sh
    @reboot python3 /home/pi/script/runCamera_1.py
    @reboot python3 /home/pi/script/runCamera_2.py
    @reboot python3 /home/pi/script/runCamera_py.py
    @reboot python3 /home/pi/script/getCamerasAndRegister.py
    10 03 * * * python3 /home/pi/script/suppressFiles.py
    10 02 3 */2 * sh /home/pi/script/certbotRenew.sh
    10 04 * * 1 sh /home/pi/script/updateAndUpgradeAuto.sh
    @reboot python3 /home/pi/script/mail_reboot.py
    */10 * * * * python3 /home/pi/script/ipcheck.py
    ```      
## Accès à la Raspberry depuis son téléphone mobile
- Différentes applications permettent d'accéder en ssh à un ordinateur distant depuis son téléphone mobile.
- Termius est une application simple dont la version gratuite est amplement suffisante pour ce projet.
## Accès au site
- Depuis l'extérieur du réseau, le site est accessible à l'adresse : `<nom du site>/camera`
- Depuis le réseau local, le site est accessible à l'adresse : `<adresse Ip locale>:54321/camera`
