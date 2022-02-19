---
title: "Tutoriel : Partie 3 - Installation de Django"
date: 2021-01-23T23:45:35+01:00
draft: false
---

## A faire
- Créer un environnement virtuel pour y installer Django
- Installer Django
- Créer un projet Django et une application
- Procéder à certains réglages de Django
- Créer les modèles et les vues de l'application
- Créer des fichiers css et html (templates)
- Capturer et stocker des images fixes prises par les caméras
- Lancer le site
## Dossiers et environnement virtuel
- Pour éviter des problèmes de conflit entre python2 et python3, il est préférable d’installer Django dans un environnement virtuel.
- De manière à structurer les dossiers nous allons utiliser une arborescence de ce type :  
{{< figure src="/media/tree1.png">}}
- C’est dans folder que nous allons créer un environnement virtuel que nous appellerons folder_venv.
Django sera installé dans cet environnement virtuel.
- Puis nous créerons un projet Django dans le dossier folder. Ce projet s’appellera project.
- Dans ce projet, nous créerons une application que nous appellerons camera.
- Vous pouvez choisir les noms folder et project que vous souhaitez (mais cela n'est pas souhaitable), à condition de les modifier dans le fichier configuration.ini (section `[paths]`, clés `folder` et `project`).
- Il est très vivement conseillé de ne pas modifier le nom de l’application camera, sinon vous devrez changer le nom de l’application dans différents fichiers html ou python que nous créerons plus tard.
## Création d’un environnement virtuel
- Créer le dossier folder
    ```sh
    mkdir ~/folder
    ```
- Créer l’environnement virtuel
    ```sh
    cd ~/folder
    python3 -m venv folder_venv
    ```
    *(Ne pas omettre le 3 de python)*
- Activer l’environnement virtuel
    ```sh
    source ~/folder/folder_venv/bin/activate
    ```
- L’invite de commande ne sera plus du type :
    ```sh
    pi@Foo:~$
    ```
    mais du type
    ```sh
    (folder_venv) pi@Foo:~$
    ```
***N.B. : dorénavant, lorsque les commandes seront tapées dans l’environnement virtuel, elles seront précédées du symbole (venv)***
- Pour désactiver l’environnement virtuel taper la commande deactivate

      (venv) deactivate

## Installation de Django
- Se mettre en environnement virtuel :
    ```sh
    source ~/folder/folder_venv/bin/activate
    ```
- Installer Django
    ```sh
    (venv) python -m pip install Django
    ```
- Django va s’installer dans l’environnement virtuel. Ici le 3 de la commande python n’est plus utile car il n’y a plus d’ambiguïté de choix, seul python3 étant installé dans l’environnement virtuel.
- Vérifier l’installation et la version
    ```sh
    (venv) python -m django --version
    ```
qui doit renvoyer une sortie du type : 4.0.2 (en fonction de la version)
## Création du projet et de l’application
### Créer le projet project
- Se mettre dans le répertoire folder (en environnement virtuel)
    ```sh
    (venv) cd ~/folder
    ```
- Créer le projet
    ```sh
    (venv) django-admin startproject project
    ```
- L’arborescence du dossier folder est la suivante :
{{< figure src="/media/tree2.png">}}
### Créer l’application camera 
- Se mettre dans le même dossier que celui contenant manage<span></span>.py,
    ```sh
    (venv) cd ~/folder/project
    ```
- Créer l’application
    ```sh
    (venv) python manage.py startapp camera
    ```
- Django a créé un nouveau répertoire. L’arborescence est :  
{{< figure src="/media/tree3.png">}}
### Structure de l’application camera
L’application camera va comporter huit vues, c’est à dire huit pages web différentes.
- accueil : la page d’accueil du site.
- historique : page présentant des photos prises à intervalle régulier par les trois caméras, sur une durée déterminée (par exemple, toutes les 5 minutes sur les 24 dernières heures)
- parHeure : page présentant toutes les photos prises sur une durée déterminée (par exemple, toutes les minutes sur les douze dernières heures)
- nuit : page présentant toutes les photos prises sur une durée déterminée (par exemple, toutes les minutes sur les douze dernières heures)
- stream_1 : flux vidéo en direct de la première caméra
- stream_2: flux vidéo en direct de la deuxième caméra
- stream_py : flux vidéo en direct de la caméra py
- stream_AllCam : flux vidéo en direct des trois caméras
## Réglage du fichier settings<span></span>.py
- Ouvrir le fichier settings.py (vous n’avez pas besoin d’être en environnement virtuel)
    ```sh
    nano ~/folder/project/project/settings.py
    ```
- Apporter les modifications suivantes
  
- ALLOWED_HOSTS : ajouter l'IP locale de la Raspberry
    ```python
    ALLOWED_HOSTS = ['<local IP raspberry>']
    ```
      par exemple `['192.168.1.49']`
- INSTALLED_APPS : ajouter 'camera.apps.CameraConfig' dans la liste existante
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
Ceci permet de régler des problèmes de prise en compte des dates par la base de données. Si vous optez pour une base de données autre que sqlite3, vous devrez réécrire les parties des scripts qui font appel au module sqlite3.
- LANGUAGE_CODE et TIME_ZONE : adapter la langue et la time-zone
    ```python
    LANGUAGE_CODE ='fr'
    TIME_ZONE = 'Europe/Paris'
    ```
- STATICFILES_DIRS :  ajouter en fin de fichier (en dessous de la ligne STATIC_URL par exemple)
    ```python
    STATICFILES_DIRS = [
      BASE_DIR / "static", 
      "/var/www/stock",
      ]
    ```
si vous avez gardé cette valeur de la clé `stock`de la section `[paths]` du fichier de configuration.  
C'est dans ce dossier `/var/www/stock` que seront stockées les photos prises par les caméras.
## Créer les modèles de l’application
- Les modèles vont permettre de définir les tables de la base de données.
- Nous allons créer deux modèles :
  - un modèle Appareil qui caractérise chaque caméra
  - un modèle Photo qui caractérise les photos qui vont être stockées
- Ouvrir le fichier ~/folder/project/camera/models<span></span>.py
    ```sh
    nano ~/folder/project/camera/models.py
    ```
- Supprimer son contenu
- Remplacer son contenu par celui du fichier models<span>.py</span> disponible [ici]({{< ref "/script/models_py.md" >}} "models.py").
- Prendre en compte les modifications ; on crée la base de données et on effectue les migrations (en environnement virtuel)
    ```sh
    (venv) python ~/folder/project/manage.py makemigrations
    (venv) python ~/folder/project/manage.py migrate
    ```
- Créer les trois caméras
	- Ouvrir le shell 
      ```sh
      (venv) python ~/folder/project/manage.py shell
      ```
	- Créer les caméras
      ```sh
      >>> from camera.models import Appareil 
      >>> c = Appareil(name="Cam_1")
      >>> c.save()
      >>> c = Appareil(name="Cam_2")
      >>> c.save()
      >>> c = Appareil(name="Cam_py")
      >>> c.save()
      ```
	- Vérifier que les trois caméras sont bien crées
      ```sh
      >>> Appareil.objects.all()
      <QuerySet [<Appareil: Cam_1>, <Appareil: Cam_2>, <Appareil: Cam_py>]>
      ```
	- Quitter le shell : `Ctrl+D`
- Nous n’avons pas utilisé l’interface Admin de Django. Celle-ci nous est inutile, toutes les actions sur la base de données se feront directement par des scripts python.
## Modifier le fichier urls<span></span>.py de ~/folder/project/project
- Ouvrir le fichier
    ```sh
    nano ~/folder/project/project/urls.py
    ```
- Modifier la ligne d'import et la ligne urlpatterns de la manière suivante
    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
      path('camera/', include('camera.urls')),
      path('admin/', admin.site.urls),
      ]
    ```
- Un exemplaire du fichier est disponible [ici]({{< ref "/script/urls_py_project.md" >}} "urls project").
## Créer un fichier urls<span></span>.py dans ~/folder/project/camera
- Créer et ouvrir le fichier en écriture
    ```sh
    nano ~/folder/project/camera/urls.py
    ```
- Coller/copier dans ce fichier le contenu du fichier urls<span></span>.py (camera) disponible [ici]({{< ref "/script/urls_py_camera.md" >}} "urls camera").
## Modifier le fichier views.py dans ~/folder/project/camera
### Modifier le fichier
- Ouvrir le fichier  
    ```sh
      nano ~/folder/project/camera/views.py
    ```
- Effacer son contenu et copier/coller le contenu du fichier views<span></span>.py (V1) disponible [ici]({{< ref "/script/views_py_V1.md" >}} "views.py V1").
### Commentaires sur ce fichier
- La vue historique (def historique(request)) permet de visualiser les captures de photos des trois caméras sur les N dernières heures en ne sélectionnant qu’une photo sur n, les photos étant prises à une fréquence f. Les paramètres N, n et f sont modifiables dans le fichier de configuration. Il s’agit des clés `historique`, `display_jour` et `capture` de la section `[fréquences]`. Si la clé historique est à 5, la clé display_jour à 2 et la clé capture à 60 cela signifie que les caméras prennent une photo toutes les 60 secondes et qu’on visualisera sur les 2 derniers jours une photo sur cinq (c’est à dire une photo toutes les 300 secondes).
- La vue parHeure (def parHeure(request)) permettra de visualiser toutes les photos des trois caméras sur les N dernières heures prises à la fréquence f, sans sélection. N et f ont la même valeur que dans la vue historique. La présentation se fera en pagination.
- La vue nuit permet de visualiser les captures de photos entre le coucher du soleil et le lever du lendemain. Les photos sont prises à la fréquence f (la même que dans la vue historique) et on peut ne sélectionner qu’une photo sur p, p étant la clé `nuit` de la section `[fréquences]` du fichier de configuration.
- Les fonctions de streaming n’appellent aucun réglage, sauf l’adresse IP locale de la raspberry (clé `raspIP` de la section `[hosts]` et les ports de sortie des flux (clés `cam_1_port`, `cam_2_port` et `cam_py_port` de la section `[camera]`)
- Par défaut : N = 24 heures (clé display_jour=1, soit 24 heures), n = 4, p = 3, f = 60 (en secondes) ; les ports des flux sont par défaut 8081, 8082 et 8084.
### Lever et coucher du soleil
- Les heures de lever et de coucher du soleil sont calculées à l'aide du module `suntimes`
- Installer le module suntimes (en environnement virtuel)  
    ```sh
    (venv) pip install suntimes
    ```
- Si besoin installer jdcal et tzlocal (*a priori* les dépendances s'installent automatiquement)
    ```sh
    (venv) pip install jdcal
    (venv) pip install tzlocal
    ```
- Le constructeur `SunTimes` du module `suntimes` prend trois paramètres de localisation : longitude, latitude et altitude qu'il faut modifier dans le fichier de configuration.
- Ouvrir le fichier de configuration
    ```sh
    sudo nano /etc/camera/configuration.ini
    ```
- Dans la section `[locate]` modifier les valeurs par défaut par celles de votre lieu. Ces valeurs sont disponibles sur [geoportail](https://www.geoportail.gouv.fr/) ou sur [google earth](https://earth.google.com/web/).
### **A renseigner impérativement dans le fichier de configuration**
- Dans la section `[hosts]` chercher la clé `raspIP`
- Remplacer la valeur <local IP Raspberry> par l'IP locale de votre Raspberry
## Créer les fichiers css et un fichier logo
- Création des dossiers css et logo
  - Les fichiers css sont situés dans `~/folder/project/camera/static/camera/css/`  
  - Ce chemin paraît compliqué à première vue, mais il est le chemin recommandé dans les différentes tutoriels relatifs à Django. On suit cette procédure, même si la simplicité du site (une seule application) ne la justifie pas.
  - Création des dossiers
    ```sh
    cd ~/folder/project/camera
    mkdir static static/camera static/camera/css static/camera/logo
    ```
- Remarques sur les fichiers css : ces fichiers ont été récupérés à partir d'un site personnel construit antérieurement. Ceci explique :
  - que les fichiers soient multiples
  - qu'il y a des redondances et des classes superflues
- Vous pouvez, bien sûr, modifier à votre convenance le css. Il faudra alors modifier l'appel des fichiers css dans le fichier `base.html` (chapître suivant).
- Création de general.css
  - Créer et ouvrir en écriture le fichier general.css
     ```sh 
     cd ~/folder/project/camera/static/camera/css/
     nano ~/folder/project/camera/static/camera/css/general.css
    ```
  - Copier/coller dans l'éditeur de texte le contenu du fichier `general.css`disponible [ici]({{< ref "/script/general_css.md" >}} "general.css")
- Création des autres fichiers css en procédant de même pour les fichiers
  - `bouton.css` dont le contenu est disponible [ici]({{< ref "/script/bouton_css.md" >}} "bouton.css")
  - `menu.css` dont le contenu est disponible [ici]({{< ref "/script/menu_css.md" >}} "menu.css")
  - `disposition.css` dont le contenu est disponible [ici]({{< ref "/script/disposition_css.md" >}} "menu.css")
  - `header_footer.css` dont le contenu est disponible [ici]({{< ref "/script/header_footer_css.md" >}} "menu.css")
  - `pagination.css` dont le contenu est disponible [ici]({{< ref "/script/pagination_css.md" >}} "pagination.css")
- Logo favicon  
  - La favicon est une image qui s'affiche dans la barre d'adresse web en regard de l'URL.
  - Charger sur la Raspberry une image au format png d'environ 40x40 pixels
  - Nommer l'image logo<span></span>.png
  - Déplacer l'image dans le dossier `~/folder/project/camera/static/camera/logo`
  - Pour charger l'image logo.png située dans votre dossier /home/user/Bureau de votre ordinateur (par exemple) vers le dossier de la Raspberry taper dans un terminal la commande suivante :
    ```sh
    scp /home/user/Bureau/logo.png pi@<local IP Raspberry>:/home/pi/folder/project/camera/static/camera/logo
    ```
  - En modifiant les chemins et l'IP de la Raspberry en fonction de vos paramètres ; à l'invite de commande, entrer le mot de passe de la Raspberry.
## Créer les fichiers html (templates)
- Création du dossier templates
  - Les fichiers html sont situés dans `~/folder/project/camera/templates/camera/`
  - Création des répertoires :
    ```sh
    cd ~/folder/project/camera
    mkdir templates templates/camera 
    ```
- A propos de base.html
  - base.html est le template (gabarit) de base dont vont hériter les autres templates.
  - C’est dans ce gabarit que sont appelés les fichiers css et la favicon. Si vous avez modifié le chemin des fichiers css, c’est dans base.html que vous devez reporter ces modifications.
  - De même, c’est dans ce gabarit que vous pouvez modifier l’aspect du menu, du header ou du footer (notamment, le nom qui apparaît en bas de page et le logo).
  - Si vous modifiez le nom de ce gabarit ou si votre application ne s’appelle pas camera, vous devrez modifier en conséquence la première ligne `{% extends "camera/base.html" %}` des autres gabarits.
- Création de base.html
  - Créer et ouvrir en écriture le fichier base.html
    ```sh
    nano ~/folder/project/camera/templates/camera/base.html
    ```
  - Copier/coller dans ce fichier le contenu du fichier `base.html` disponible [ici]({{< ref "/script/base_html.md" >}} "base.html")
- Procéder de même pour les autres fichiers html
    - `accueil.html` dont le contenu est disponible [ici]({{< ref "/script/accueil_html.md" >}} "accueil.html")
    - `historique.html` dont le contenu est disponible [ici]({{< ref "/script/historique_html.md" >}} "historique.html")
    - `nuit.html` dont le contenu est disponible [ici]({{< ref "/script/nuit_html.md" >}} "nuit.html")
    - `parHeure.html` dont le contenu est disponible [ici]({{< ref "/script/parHeure_html.md" >}} "parHeure.html")
    - `stream_1.html` dont le contenu est disponible [ici]({{< ref "/script/stream_1_html.md" >}} "stream_1.html")
    - `stream_2.html` dont le contenu est disponible [ici]({{< ref "/script/stream_2_html.md" >}} "stream_2.html")
    - `stream_py.html` dont le contenu est disponible [ici]({{< ref "/script/stream_py_html.md" >}} "stream_py.html")
    - `stream_AllCam.html` dont le contenu est disponible [ici]({{< ref "/script/stream_AllCam_html.md" >}} "stream_AllCam.html")
## Capturer les images et les stocker
### Créer les répertoires de stockage
- Créer le répertoire /var/www/stock
    ```sh
    sudo mkdir /var/www/stock
    ```
- Créer les sous-répertoires pour les différentes caméras
    ```sh
    cd /var/www/stock
    sudo mkdir Camera_1 Camera_2 Camera_py 
    ```
- Changer le propriétaire de /var/www/stock
    ```sh
    sudo chown -R pi /var/www/stock
    ```
### Ecrire le script de capture des photos
- Ce script sera lancé au démarrage et tournera en boucle en effectuant :
  - la capture des images pour chaque caméra à la fréquence choisie
  - l'inscription dans la base de données des caractéristiques relatives à chaque photo (caméra, date de prise, nom de la photo, répertoire de stockage)
- Créer le script
  - Créer et ouvrir en écriture le fichier getCamerasAndRegister<span></span>.py
    ```sh
    nano ~/script/getCamerasAndRegister.py
    ```
  - Copier/coller dans ce fichier le contenu du fichier `getCamerasAndRegister.py` disponible [ici]({{< ref "/script/getCamerasAndRegister_py.md" >}} "getCamerasAndRegister.py")
- Lancer le script au démarrage de la Raspberry
  - Ouvrir le cron en édition
    ```sh
    crontab -e
    ```
  - Ajouter la ligne suivante
    ```sh
    @reboot python3 /home/pi/script/getCamerasAndRegister.py
    ```
### Ecrire le script de destruction périodique des photos
- Tous les jours on efface les images datant de plus de N jours, N étant la clé `delay-delete` de la section `[frequences]` du fichier de configuration.
- Par défaut, la valeur de N est 2, c’est à dire qu’on ne conserve les images que deux jours.
- Il est indispensable d’effectuer cette tâche régulièrement afin que la carte micro-SD ne soit pas saturée.
- Créer et ouvrir en écriture le fichier suppressFiles<span></span>.py
    ```sh
    nano ~/script/suppressFiles.py
    ```
- Copier/coller dans ce fichier le contenu du fichier `suppressFiles` disponible [ici]({{< ref "/script/suppressFiles_py.md" >}} "suppressFiles.py")

- Lancer le script tous les jours à 03H10 du matin (par exemple) dans le crontab
	- Ouvrir le cron en édition
    ```sh
    crontab -e
    ```
  	- Ajouter la ligne suivante
    ```sh
    10 03 * * * python3 /home/pi/script/suppressFiles.py
    ```
## Lancer Django au démarrage
- Le script lance le serveur de Django au démarrage de la raspberry sur le port 8000 par défaut (paramétrable dans /etc/configuration.ini)
- *Pour accéder au site depuis un appareil du réseau, vous devez avoir indiqué l’adresse IP locale de la raspberry dans ALLOWED_HOSTS du fichier ~/folder/project/project/settings.py (par exemple ALLOWED_HOSTS = ['192.168.1.49'])*
- Créer et ouvrir en écriture le fichier runDjango<span></span>.py
    ```sh
    nano ~/script/runDjango.py
    ```
- Copier/coller le contenu du fichier runDjango<span></span>.py disponible [ici]({{< ref "/script/runDjango_py.md" >}} "runDjango.py")
- Lancer le script au démarrage dans le crontab
  - Ouvrir le crontab en édition
    ```sh
    crontab -e
    ```
  - Ajouter la ligne suivante
    ```sh
    @reboot python3 /home/pi/script/runDjango.py
    ```
## Tester le site
- Rebouter le système
    ```sh
    sudo reboot
    ```
- Attendre que les scripts des différentes caméras soient lancés.
- Dans la barre d'adresse d'un navigateur taper `<local IP Raspberry>:8000/camera/` (par exemple : `192.168.1.1:8000/camera/`)
- Vous devez obtenir ce résultat :
{{< figure src="/media/cam_accueil.png">}}
- Si les caméras sont bien lancées, vous devez voir les flux en cliquant sur le bouton `En direct`. Bien sûr, pour les autres pages html, au début vous ne verrez que peu ou pas d'images. 
- Au fil du temps, les différents historiques (Histoire, Heure par Heure et Nuit) pourront être longs à s'afficher, le nombre d'images à charger étant élevé. *C'est, à l'évidence, une faiblesse des scripts.*
## A ce stade - Prochaine étape
### A ce stade
- On dispose d'un site web qui fonctionne en local avec le serveur embarqué de Django.
- Ce site est accessible depuis les différents appareils du réseau local en tapant dans la fenêtre d'un navigateur web  `<local IP Raspberry>:<port serveur Django>/camera`
- Si vous ne souhaitez pas accéder au site depuis l'extérieur, vous pouvez, de manière peu orthodoxe, en rester là. Mais il est souhaitable de passer à l'étape suivante.
### Prochaine étape
- Installation d'un serveur Apache qui va prendre la main sur le serveur embarqué de Django.
- Installation du module mod-wsgi, interface entre Apache et Django
- Paramétrages de Apache et Django pour que le site soit accessible en production (et non plus en développement).

