---
title: "Tutoriel : Partie 7 - Fichiers de gestion"
date: 2021-01-25T10:33:28+01:00
draft: false
---

## A faire
- Ecriture de scripts de gestion
- Lancement des scripts depuis le cron
- Pouvoir se connecter en ssh à la raspberry depuis son téléphone mobile
## Mise à jour régulière du système
- Créer et ouvrir le fichier en écriture
    ```sh
    nano ~/script/updateAndUpgradeAuto.sh
    ```
- Ecrire le script en ajoutant les deux lignes
    ```sh
    #!bin/bash  
    sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y
    ```
## Etre informé par courriel des redémarrages de la raspberry
- A chaque démarrage de la raspberry, un courriel est envoyé pour prévenir l'utilisateur.  
- Ceci permet notamment de vérifier que les caméras se sont bien lancées.  
- Les adresses mail de l'envoyeur et du destinataire (elles peuvent être différentes) ainsi que le mot de passe sont paramétrables dans configuration<span></span>.ini.  
- Créer et ouvrir le script en écriture
    ```sh
    nano ~/script/mail_reboot.py
    ```
- Copier/coller le contenu du fichier `mail_reboot.py` disponible [ici]({{< ref "/script/mail_reboot_py.md" >}} "mail_reboot.py")
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

## Lancement des différents scripts dans le cron
- Éditer le crontab
    ```sh
    crontab -e
    ```
- Lancer le script de mise à jour tous les lundis à 4H10 en ajoutant la ligne
    ```sh
    10 04 * * 1 sh /home/pi/script/updateAndUpgradeAuto.sh
    ```    
- Lancer l'envoi de courriel au redémarrage de la Raspberry en ajoutant la ligne
    ```sh
    @reboot python3 /home/pi/script/mail_reboot.py
    ```
- Lancer le script de contrôle de l'IP en ajoutant la ligne
    ```sh
    */10 * * * * python3 /home/pi/script/ipcheck.py
    ```
	L'IP sera contrôlée toutes les 10 minutes.
- Au final le cron doit ressembler à ceci
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
## Accès à la raspberry depuis son téléphone mobile
- Il peut être nécessaire de se connecter à la raspberry pour modifier certains paramètres ou pour toute autre raison. Y compris depuis l’extérieur du réseau avec son téléphone mobile.
- Différentes applications permettant une connexion ssh depuis un mobile sont disponibles. Termius est particulièrement simple et a une offre gratuite amplement suffisante pour ce projet. 
- Installer `Termius` depuis l'[App Store](https://apps.apple.com/fr/app/termius-ssh-client/id549039908) ou [Google Play](https://play.google.com/store/apps/details?id=com.server.auditor.ssh.client)
- Une fois `Termius` installée sur son mobile
  - Dans le menu choisir Hosts
  - Créer un nouvel hôte en appuyant sur + et choisir `New host`
  - Vous pouvez créer deux hôtes : un accès en réseau local et un accès depuis l’extérieur
  - Accès extérieur
    - Alias : rentrer l’étiquette de votre choix, par exemple : `Camera Ext`
    - Hostname or IP Address : entrer l’ adresse IP de votre box
    - Chosir le mode SSH en cliquant sur la case (a priori sélectionné par défaut)
    - Port : entrer le port externe que vous avez attribué pour le ssh dans le NAT/PAT
    - Username : pi (à moins que vous n’ayez changé de nom d’utilisateur)
    - Password : entrer le mot de passe de la raspberry (en faisant un copier/coller)
    - Valider en cliquant sur le symbole `∨` en haut à droite de l’écran
  - Accès local
    - Alias : rentrer l’étiquette de votre choix, par exemple : `Camera Local`
    - Hostname or IP Address : entrer l’ adresse IP locale de la raspberry (par exemple 192.168.1.49)
    - Chosir le mode SSH en cliquant sur la case (a priori sélectionné par défaut)
    - Port : 22, qui est le port par défaut
    - Username : pi (à moins que vous n’ayez changé de nom d’utilisateur)
    - Password : entrer le mot de passe de la raspberry (en faisant un copier/coller)
    - Valider en cliquant sur le symbole `∨` en haut à droite de l’écran
  - A la première connexion, le logiciel demande de valider la clé : appuyer sur `Connect`
  - Lors des changements d’IP de la box, il faut changer l’adresse IP de l’hôte de l’accès extérieur.
## Conclusion
Un système de surveillance en flux direct et avec enregistrement et stockage de photos a été mis en place pour être consultable, après authentification, depuis le web en utilisant mjpg-streamer, django et apache.  
En jouant sur différents paramètres, notamment la fréquence de capture des images, on dispose, si on le souhaite, d’une surveillance qui peut être adaptée à d'autres projets.  
Certaines faiblesses sont patentes ; par exemple le fait que si l'une des caméras ne se lance pas au départ, il n'y a ni procédure de relance ni message d'alerte.  
De manière délibérée, il n'a pas été fait appel à un logiciel de détection de mouvements ni à un traitement des images permettant de ne sélectionner que les photos sur lesquelles un cheval apparaîtrait. Ceci pourrait faire l’objet d'autres projets.  
Toutes vos remarques et critiques sont les bienvenues et peuvent être adressées par courriel à l'adresse suivante : `pmathis@protonmail.com`.
