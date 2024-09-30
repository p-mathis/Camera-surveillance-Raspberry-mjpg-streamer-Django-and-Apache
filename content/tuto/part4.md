---
title: "Tutoriel : Partie 4 - Installation de Apache et mod-wsgi"
date: 2021-01-24T18:14:33+01:00
draft: false
---

## A faire
- Installer le serveur Apache sur la raspberry
- Installer et activer le module mod-wsgi, qui va servir d'interface entre Django et Apache
- Créer un fichier de configuration de site et l'activer
- Restreindre l'accès au site en forçant l'authentification de l'utilisateur

## Installation de Apache
- Mise à jour de raspbian si l'installation n'est pas récente
    ```sh
    sudo apt update
    sudo apt upgrade
    ```
- Installation de apache (répondre `Oui` aux invites de commande)
    ```sh
    sudo apt install apache2
    ```
- Vérifier l'installation et la version
    ```sh
    sudo apache2ctl -v
    ```
- Vérifier la page d'accueil de apache en tapant `<local IP Raspberry>:80` dans la barre d'un navigateur, vous devez voir la page d'accueil de Apache (80 est le port par défaut du serveur apache).

## Copie de différents fichiers de configuration
- Avant de modifier différents fichiers de configuration de apache2, il est souhaitable de faire une copie du fichier original, par exemple en ajoutant ORIGINAL en fin de nom du fichier.
- Copie des fichiers apache2.conf, security.conf, localized-error-pages.conf
    ```sh
    sudo cp /etc/apache2/apache2.conf /etc/apache2/apache2.confORIGINAL
    sudo cp /etc/apache2/conf-available/security.conf /etc/apache2/conf-available/security.confORIGINAL
    sudo cp /etc/apache2/conf-available/localized-error-pages.conf /etc/apache2/conf-available/localized-error-pages.confORIGINAL
    ```
## Sécurisation minimale du serveur apache
- Suivre les instructions de la page [wiki.debian](https://wiki.debian-fr.xyz/S%C3%A9curiser_Apache2#Limiter_les_informations_visibles)
### Modifier security.conf
- Ouvrir en écriture le fichier security.conf
    ```sh
    sudo nano /etc/apache2/conf-available/security.conf
    ```
- Modifier le fichier comme suit
  - modifier `ServerTokens Prod` (et non OS)  
  - modifier `ServerSignature Off` (et non On)  
  - laisser `TraceEnable Off`  
  - décommenter `Header set X-Content-Type-Options: "nosniff"` (enlever le #)  
  - décommenter `Header set X-Frame-Options: "sameorigin"` (enlever le #)
- Activer le module headers
  - Les lignes `Header set ...` du fichier ayant été décommentées, il faut activer le module headers
  - Activer le module
    ```sh
    sudo a2enmod headers
    ```
### Modifier la page d'accueil Apache
- Supprimer la page d'accueil et la remplacer par une nouvelle page
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
### Créer une page d'erreur 404
- Créer la page
    ```sh
    sudo nano /var/www/html/missing.html
    ```
- Copier, par exemple, le script suivant dans cette nouvelle page
    ```html
    <html>
    DOCUMENT INEXISTANT<br>
    MISSING DOCUMENT
    </html>
    ```
### Modifier /etc/apache2/conf-available/localized-error-pages.conf  
- Ouvrir le fichier en écriture
    ```sh
    sudo nano /etc/apache2/conf-available/localized-error-pages.conf
    ```
- Décommenter la ligne `ErrorDocument 404 /missing.html`
### Prendre en compte les modifications en redémarrant apache2
```sh
sudo systemctl restart apache2
```
## Installer le module mod-wsgi
- Sources
  - [djangoprojcet](https://docs.djangoproject.com/fr/2.2/howto/deployment/wsgi/modwsgi/)
  - [modwsgi](https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html)
  - [pypi.org](https://pypi.org/project/mod-wsgi/)
- Installer apxs
    ```sh
    sudo apt install apache2-dev
    ```
- Installer le module dans l’environnement virtuel
    ```sh
    (venv) pip install mod_wsgi
    ```
- Se mettre dans le répertoire des packages python de l’environnement virtuel
    ```sh
    (venv) cd /home/pi/folder/folder_venv/lib/python3.7/site-packages
    ```
  - ce chemin peut être modifié en fonction de la version de python
  - pour savoir où sont les packages de python lire le retour de la commande :
    ```sh
    (venv) python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"
    ```
- Depuis ce répertoire lancer la commande
    ```sh
    (venv) mod_wsgi-express module-config
    ```
- On obtient une sortie du type : 
    ```sh
    LoadModule wsgi_module "/home/pi/folder/folder_venv/lib/python3.7/site-packages/mod_wsgi/server/mod_wsgi-py37.cpython-37m-arm-linux-gnueabihf.so"
    WSGIPythonHome "/home/pi/folder/folder_venv"
    ```
- Copier ces deux lignes
- Vous pouvez quitter l'environnement virtuel (commande : `deactivate`)
- Créer un fichier wsgi.load dans /etc/apache2/mods-available
    ```sh
    sudo nano /etc/apache2/mods-available/wsgi.load
    ```
- Dans ce fichier coller les deux lignes récupérées précédemment :
    ```sh
    LoadModule wsgi_module "/home/pi/folder/folder_venv/lib/python3.7/site-packages/mod_wsgi/server/mod_wsgi-py37.cpython-37m-arm-linux-gnueabihf.so"
    WSGIPythonHome "/home/pi/folder/folder_venv"
    ```  
  *(A modifier en fonction de la sortie obtenue)*
- Activer le module mod-wsgi
    ```sh
    sudo a2enmod wsgi
    ```
- Redémarrer le service apache
    ```sh
    sudo systemctl restart apache2
    ```
- Le module wsgi est visible dans le dossier `/etc/apache2/mods-enabled`
## Donner les droits à www-data et à l'utilisateur pi
- *L'attribution des droits sous linux est une plaie sans nom. Les droits attribués ici ne sont pas nécessairement les plus pertinents, mais ils permettent un bon fonctionnement du serveur. Une mauvaise attribution des droits peut empêcher d'accéder au site, de visualiser les images ou de bénéficier de la présentation du css.*
- Créer un groupe varwwwusers composé de pi et de www-data
    ```sh
    sudo group add varwwwusers
    ```
- Ajouter pi et www-data au groupe varwwwusers
    ```sh
    sudo adduser pi varwwwusers
    sudo adduser www-data varwwwusers
    ```
	*(www-data est l'utilisateur qui exécute Apache et qui appartient au groupe www-data)*
- Changer le propriétaire du répertoire /var/www/stock et de ses sous-répertoires
    ```sh
    sudo chown -R pi:varwwwusers /var/www/stock
    ```
- Modifier les droits lecture/écriture/éxecution (rwx) de /var/www/stock et de ses sous-répertoires
    ```sh
      sudo chmod -R 750 /var/www/stock
    ```
- Modifier le propriétaire du fichier ~/folder/project/db.sqlite3
    ```sh
    sudo chown pi:www-data ~/folder/project/db.sqlite3
    ```
- Modifier les droits rwx du fichier ~/folder/project/db.sqlite3
    ```sh
    sudo chmod 770 ~/folder/project/db.sqlite3
    ```
## Créer un fichier de configuration de site et l’activer
- On va créer dans `/etc/apache2/sites-available` un fichier de configuration de site. On peut donner le nom que l'on veut à ce fichier. J'ai choisi project-camera.conf et il est **fortement conseillé de ne pas changer ce nom**, sinon il faudra le modifier au sein même du fichier lorsqu'il apparaît.
- Créer et ouvrir en écriture le fichier de configuration de site (appelé `project-camera.conf`)
    ```sh
    sudo nano /etc/apache2/sites-available/project-camera.conf
    ```
- Copier/coller dans ce fichier le contenu du fichier `project-camera.conf_V1` disponible [ici]({{< ref "/script/project-camera_conf_V1.md" >}} "project-camera_V1.html")
- Modifications à apporter
	- `ServerName` : mettre l'adresse IP locale de la Raspberry
	- Modifier les différents chemins de fichiers si vous n'avez pas gardé les chemins par défaut
- Enregistrer et quitter : `Ctrl+0 - Entrée - Ctrl+X` (sous nano)
- Activer le site 
    ```sh
    sudo a2ensite project-camera
    ```
- Activer la nouvelle configuration 
    ```sh
    sudo systemctl reload apache2
    ```
- On aura un accès au site sur le port 80, qui est le port par défaut de Apache.

## Copier les fichiers statiques
- Pour que Apache lise les fichiers statiques (css et logo) de l'application caméra, il faut les déplacer dans `/var/www/stock`
- Méthode collectstatic (déconseillée)
  - cette méthode utilise la commande collectstatic du script manage<span></span>.py
    ```sh
    (venv) python ~/folder/project manage.py collectstatic
    ```
  - L'inconvénient est que les images déjà stockées sont considérées comme statiques par Django et qu'elles seront à nouveau copiées !
- Méthode manuelle (conseillée)
  - Le nombre de fichiers statiques étant limité, le plus simple est de les transférer manuellement
  - Lancer la commande (inutile d'être en sudo, le dossier de destination apprtenant maintenant à l'utilisateur pi)
    ```sh
    cp -r ~/folder/project/camera/static/camera /var/www/stock
    ```
  - L'arborescence du dossier `/var/www/stock` doit être la suivante  
{{< figure src="/media/tree4.png">}}
## Modifier le fichier settings<span></span>.py
- Ouvrir en écriture le fichier settings.py
    ```sh
    nano ~/folder/project/project/settings.py
    ```
- Mettre la valeur `DEBUG` à `False`
    ```python
      DEBUG = False
    ```
- Masquer la clé de sécurité
  - Copier la valeur de `SECRET_KEY` 
  - Créer et ouvrir en écriture /etc/camera/secret_key.txt  
    ```sh
    sudo nano /etc/camera/secret_key.txt
    ```
  - Coller la valeur de `SECRET_KEY` dans ce fichier
- Remplacer la ligne `SECRET_KEY = '<votre SECRET_KEY>'` par
    ```python
      with open(‘/etc/camera/secret_key.txt’) as f:
        SECRET_KEY = f.read().strip()
  ```
- STATICFILES_DIRS : Modifier ainsi le contenu (en l'adaptant éventuellement en fonction des chemins des dossiers)
    ```python
    STATICFILES_DIRS = [  
    BASE_DIR / "/home/pi/folder/project/camera/static",  
      "/var/www/stock"  
      ] 
  ```
## Nouvel accès au site
- Redémarrer apache pour prendre en compte les modifications
    ```sh
    sudo systemctl restart apache2
    ```
- Accéder au site depuis un navigateur web en tapant `<local IP Raspberry>/camera` (par exemple : `192.168.1.49/camera`)
L'accès se fait par le port par défaut de Apache (80) qu'il est inutile de préciser
- Supprimer l'accès par le serveur de Django
  - Le serveur de Django est maintenant inutile ; on peut supprimer ou commenter sa ligne de commande dans le crontab
  - Ouvrir le crontab en écriture
    ```sh
    crontab -e
    ```
  - Commenter (ou supprimer) la ligne
    ```sh
    #@reboot python3 /home/pi/script/runDjango.py
    ```
  - Au prochain démarrage de la Raspberry, le serveur de Django ne se lancera plus.
## Restreindre l'accès au site
### Intérêt
- Tant que l'on est en réseau local, la restriction de l'accès au site n'est pas indispensable
- Elle le deviendra dès que le site sera accessible de l'extérieur du réseau, sinon n'importe qui pourra visionner le flux et les images des caméras depuis n'importe où !
- On peut aussi avoir intérêt à restreindre cet accès même dans le réseau local.
### Déclarer les utilisateurs autorisés
- En passant par l'authentification de Django
  - Django possède les outils pour forcer une authentification des usagers pour l'accès à un site.
  - La procédure est expliquée dans [djangoproject](https://docs.djangoproject.com/fr/3.1/howto/deployment/wsgi/apache-auth/)
  - Cette méthode a échoué me concernant, soulevant une erreur `AppRegistryNotReady: Apps aren't loaded yet` que je n'ai pas réussi à réparer.
- Avec un fichier .htaccess de Apache
  - Créer le fichier .htaccess dans /etc/apache2
    ```sh
    sudo touch /etc/apache2/.htpasswd
    ```
  - Créer un utilisateur, par exemple `bar`
    ```sh
    sudo htpasswd /etc/apache2/.htpasswd bar
    ```
  - A l'invite de commande `New password:`, rentrer un mot de passe, éventuellement en le copiant/collant ; attention, rien ne s'affiche (c'est normal) ; puis valider avec la touche `Entrée`.
  - A l'invite de commande `Re-type new password:`, rentrer à nouveau le mot de passe.
  - Le message `Adding password for user bar` s'affiche. 
  - Créer autant d'utilisateurs que nécessaire en procédant de la même manière.
### Modifier le fichier project-camera.conf
- Il faut déclarer dans le fichier de configuration du site la restriction d'accès.
- Ouvrir le fichier en écriture
    ```sh
    sudo nano /etc/apache2/sites-available/project-camera.conf
    ```
- Le modifier en ajoutant avant la balise de fermeture `</VirtualHost>`
    ```sh
	<Location "/">
  	AuthType Basic
  	AuthName "Authentification obligatoire"
  	AuthUserFile "/etc/apache2/.htpasswd"
  	Require valid-user
	</Location>
    ```
- Le fichier doit ressembler au contenu du fichier project-camera.conf_V2 disponible [ici]({{< ref "/script/project-camera_conf_V2.md" >}} "project-camera_V2.html").
- Cette modification oblige le client à s'identifier lorsqu'il veut atteindre les pages sous l'url `/`, c'est à dire la totalité du site.
### Modifier le fichier wsgi.py
- Pour des raisons obscures, Apache soulève l’erreur suivante si on tente d’accéder au site sans modifier le fichier wsgi.py
    ```sh
    ModuleNotFoundError: No module named 'project'
    ```
- Pour réparer cette erreur, ouvrir le fichier wsgi.py
    ```
      nano ~/folder/project/project/wsgi.py
    ```
- Et ajouter les trois lignes suivante
    ```python
    import sys
    sys.path.append('/home/pi/folder/project')
    sys.path.append('/home/pi/folder/project/project')
    ```
*(A modifier en fonction du nom et du chemin de votre projet)*
- Votre fichier doit ressembler au fichier `wsgi.py` disponible [ici]({{< ref "/script/wsgi_py.md" >}} "wsgi.py")
### Accès au site
- Relancer Apache pour qu’il prenne en compte les modifications
    ```
      sudo systemctl restart apache2
    ```
- Dans un navigateur en tapant `<local IP Raspberry/camera` (par exemple `192.168.1.49/camera`), une demande d’identification apparaît
{{< figure src="/media/identification.png">}}    
- Selon les navigateurs, vous pouvez enregistrer votre identifiant et son mot de passe.
## A ce stade - Prochaine étape
### A ce stade
- Vous disposez d’un site web qui fonctionne en local avec le serveur Apache
- Ce site est accessible depuis les différents appareils du réseau local en tapant dans la fenêtre d’un navigateur web `<Local IP Raspberry>/camera`
- Vous devez vous identifier pour accéder au site.
### Prochaine étape
- Accéder au site depuis l’extérieur du réseau
- Obtenir un nom de domaine
- Service Dyn-DNS

