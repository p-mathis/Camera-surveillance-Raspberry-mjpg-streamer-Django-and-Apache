---
title: "Tutoriel : Partie 1 - Mise en route de la Raspberry"
date: 2021-01-23T16:11:47+01:00
draft: false
---
## A faire
- Mettre en route la Raspberry
- Modifications au niveau de la box
- Assurer une connexion ssh avec la Raspberry
- Mettre en place un fichier de configuration
## Matériels et logiciels
### Les matériels
Ils ont été décrits dans la page [d'accueil]({{< ref "_index.md" >}} "Accueil").
### Les logiciels
- Raspberry Pi Imager pour installer raspbian sur la raspberry.
- Rasbpian comme OS de la raspberry.
- mjpg-streamer pour assurer les flux vidéos et les captures d’image.
- Django, cadre de développement en langage python pour développer un site web.
- Un serveur Apache
- Un service DYN-DNS pour contourner le problème des IP dynamiques et obtenir un nom de site (No-IP).
- Un service pour sécuriser les échanges de données (Certbot / Let’s Encrypt)
- Une application pour se connecter en ssh depuis un téléphone mobile (Termius)
### Coût du projet
Le coût total du projet est relativement modeste :
- raspberry kit complet avec boîtier, alimentation et carte SD : 80 €
- 2 caméras HD à port USB : 2x40 = 80€
- pi-camera avec câble connecteur = 10 €
- spot émetteur à infrarouge = 20 €  

La gamme de prix ci-dessus est plutôt dans le haut de la fourchette. On peut trouver moins cher en fonction de la qualité et, surtout, du fournisseur.
## Mise en route de la raspberry
### Création de la carte micro-SD
- Source : [raspberry-pi](https://raspberry-pi.fr/creer-carte-sd-windows-mac-linux-raspberry-pi-imager/)
- Installer Raspberry Pi Imager sur son ordinateur
  - sous [linux](https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb)
  - sous [macOX](https://downloads.raspberrypi.org/imager/imager_latest.dmg)
  - sous [Windows](https://downloads.raspberrypi.org/imager/imager_latest.exe)
- Insérer la carte micro-SD dans son ordinateur
- Lancer Raspberry Pi Imager et suivre les instructions :
  - sélectionner l’OS ; choisir raspbian
  - sélectionner la carte cible micro-SD
  - lancer l’écriture sur la carte
- Insérer la carte micro-SD dans la raspberry ***éteinte***.
### Mise en route de la raspberry et premiers réglage
- Relier la Raspberry à un écran, une souris et un clavier
- Brancher la Raspberry
- Suivre les instructions : choix de la langue, du pays...
- WiFi : accepter ou non selon que vous êtes connecté par câble ou non
- SetUp : accepter la mise à jour
- Lorsque la mise à jour est terminée, ne pas rebouter de suite : cliquer sur `Later`
- Aller dans Framboise --> Preferences --> Configuration Raspberry
- Onglet Système : laisser le nom de la Raspberry ou le changer (Foo par exemple)
- Onglet Système Bouton Modifier le mot de passe :  mettre un mot de passe fort. Effectivement, le ssh va être activé et **pour des raisons de sécurité il convient que le mot de passe soit consistant**
- Onglet Interfaces : activer la caméra et le ssh
- Cliquer sur OK
- Rebouter le système  
La Raspberry va maintenant être accessible en ssh depuis l'ordinateur. L'écran, la souris et le clavier peuvent être débranchés.
### Modifications au niveau de la box
On donne une IP locale fixe à la Raspberry et on modifie son port ssh externe.  
Les indications données ici sont valables pour une livebox Orange. La procédure est similaire chez les autres opérateurs.
- Pénéter dans les paramètres de la box
  - taper `192.168.1.1` dans la barre d'un navigateur (pour Orange)
  - s'identifier
- Assigner une IP locale fixe à la Raspberry
  - aller dans les paramètres `Réseau`
  - cliquer sur l'onglet `DHCP`
  - la Raspberry apparaît dans la section `Baux DHCP dynamiques`
  - au dessus des baux statiques, sélectionner la Raspberry dans la liste déroulante
  - les autres lignes vont se remplir automatiquement
  - cliquer sur `Ajouter`
  - la raspberry est maintenant positionnée dans la section `Baux DHCP statiques`
  - *Dans ce tutoriel, l’IP locale fixe est 192.168.1.49*
- Modifier le port ssh externe de la Raspberry
  - cliquer sur l'onglet NAT/PAT
  - dans la liste déroulante sélectionner SSH ou créer SSH en cliquant sur nouveau
  - port interne : mettre 22
  - port externe : mettre un port dont on sait a priori qu’il n’est pas utilisé, entre 40000 et 60000 par exemple
  - protocole : laisser `TCP`
  - Équipement : choisir la Raspberry dans la liste déroulante
  - IP externe : laisser `Toutes`
  - *Ceci évitera les attaques multiples de personnes malveillantes qui viseront en premier lieu le port 22 par défaut.*
### Connexion ssh à la raspberry
- Ouvrir un terminal dans l’ordinateur
  - Linux : raccourci clavier `Ctrl + Alt + T`
  - OS X : Applications > Utilitaires : choisir Terminal
  - Windows : `Touche Windows + R` pour ouvrir l’invite de commande ; puis `cmd` dans l’invite de commande.
- Taper dans le terminal :
    ```sh
    ssh pi@<local IP Raspberry>
    ```
    Par exemple : `ssh pi@192.168.1.49`
- Inutile de préciser le port : on est en local et le port par défaut est 22
- A l’invite de commande entrer le mot de passe (par copier-coller).  
***On ne travaillera plus sur la Raspberry que par le biais d'un terminal connecté à celle-ci, c'est à dire avec une ligne de commande qui commence par `pi@Foo` si votre Raspberry a été nommée `Foo`.***
### Nettoyage des dossiers
De manière non indispensable, mais pour plus de clarté, vous pouvez détruire différents dossiers de la raspberry :
```sh
rm -R Desktop Bookshelf Documents Downloads Music Pictures Public Templates Videos
```
## Utilisation d'un fichier de configuration
### Intérêt et présentation
- Ne pas coder en "dur" : dans les différents scripts utilisés, de manière à ne pas coder en dur de multiples variables, ce qui obligerait à les chercher une à une afin de les modifier, on passe par un fichier de configuration.  
- Le fichier est de type ini et il est lu dans les scripts python par `configparser`.
- Ce fichier comprend six sections :
  - [locate] : coordonnées du lieu pour le calcul des heures de lever et coucher du soleil
  - [hosts] : ip de la raspberry
  - [mails] : différentes adresses courriel, mot de passe et port smtp
  - [camera] : différents paramètres des caméras
  - [paths] : chemins des dossiers et des applications utilisés
  - [frequences] : par exemple règle la fréquence des captures des images des caméras
### Installation
- Où placer le fichier ? Comment le nommer ?
  - le placer dans un dossier `/etc/camera` 
  - le nommer `configuration.ini`
  - si vous décidez de le placer ailleurs ou de le nommer autrement, vous devrez modifier, dans tous les scripts où il est appelé, son chemin et son nom
- Création du dossier /etc/camera  
Dans le terminal connecté en ssh à la Raspberry, taper  
    ```sh
    sudo mkdir /etc/camera
    ```
	(comme /etc est un dossier appartenant à root, créer le dossier camera en sudo)
- Création et ouverture en écriture du fichier configuration.ini  
    ```sh
    sudo nano /etc/camera/configuration.ini
    ```
	Vous pouvez utiliser un autre éditeur que nano ; celui-ci a l’avantage de la simplicité.
- Copier le contenu du fichier `configuration.ini` disponible en cliquant [ici]({{< ref "/script/configuration_ini.md" >}} "configuration_ini")
- Coller ce contenu dans la fenêtre vide du terminal
- Sauvegarder et quitter en faisant
    ```sh
    Ctrl+O  
    Entrée  
    Ctrl+X  
    ``` 
## A ce stade - Prochaine étape
### A ce stade
- Raspbian est installé sur la Raspberry
- La Raspberry a une IP locale fixe
- Une connexion ssh est possible avec la Raspberry
- Un fichier de configuration a été mis en place
### Prochaine étape
- Installer mjpg-streamer
- Installer les caméras
- Ecrire les scripts permettant le lancement des caméras au démarrage de la Raspberry

