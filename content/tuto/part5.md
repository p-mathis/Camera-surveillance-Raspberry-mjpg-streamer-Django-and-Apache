---
title: "Tutoriel : Partie 5 - Accès depuis l'extérieur du réseau"
date: 2021-01-24T22:50:07+01:00
draft: false
---
## A faire
- S'inscrire à un site DynDNS et obtenir un nom de domaine
- Déclarer le site sur la box
- Configurer le site Apache
- Modifier le fichier views.py de Django
## Disposer d'une adresse mail
- Vous pouvez utiliser une de vos adresses mail existantes
- Sinon, en créer une réservée uniquement à ce projet.
- Il est préférable de choisir un opérateur qui accepte les IP dynamiques pour le protocole SMTP. Les adresses gmail ne sont pas nécessairement les meilleures à ce point de vue. laposte.net (même si c’est moins glamour) ne pose pas de problèmes de cet ordre. protonmail.com n'accepte le protocole SMTP que dans les versions payantes.
## S’inscrire à un site DynDNS et obtenir un nom de domaine
### Pourquoi et chez qui ?
- Le serveur DNS permettra de traduire le nom de domaine en adresse IP (l’IP publique de votre box).
- Les IP publiques n’étant pas nécessairement fixes, le DNS dynamique transférera l’adresse IP évolutive vers un nom de domaine fixe.
- Quelques fournisseurs de DNS dynamiques proposent des offres gratuites. Mais tous ne sont pas compatibles avec les box dont nous disposons, notamment la livebox d’Orange.
- Malgré ses contraintes (nécessité de réactiver son abonnement gratuit tous les mois) No-IP a l’avantage d’être performant. 
- La box d'Orange propose maintenant *(octobre 2023*) le protocole GnuDIP. dynu.com propose un service gratuit pour lequel il n'y a pas besoin de réactiver régulièrement le nom de domaine.
- On aurait pu prendre une autre option : acheter un nom de domaine chez un registraire pour quelques Euro par an et bénéficier du DynDNS de ce registraire. OVH est une option intéressante et un [tutoriel](https://raspberry-pi.fr/nom-domaine/) très bien fait est disponible.
- Quelque soit l’option que vous choisissez, la marche à suivre sera globalement la même.
### Obtenir un nom de domaine chez No-Ip
- Aller sur le site de [No-Ip](https://www.noip.com/)
- Créer sur la page d’accueil le nom d’hôte gratuit de votre choix
- Remplir le formulaire en indiquant son adresse mail, un mot de passe
- Valider en prenant l’inscription gratuite
- Confirmer l’inscription en validant le lien reçu sur sa boîte mail
- Connectez-vous à votre compte
- Si vous consultez votre `Tableau de bord` vous avez les informations sur votre site : le nom, la date d’expiration (vous devrez réactiver votre abonnement à l’échéance), l’adresse IP cible (celle de votre box).
### Obtenir un nom de domaine chez dynu.com
- Aller sur la page d'inscription de [dynu.com](https://www.dynu.com/fr-FR/ControlPanel/CreateAccount)
- Remplir le formulaire en indiquant son adresse mail, un mot de passe (entre 4 et 20 caractères)
- Cliquer sur `Soumettre`
- Confirmer l'adresse mail via le mail de vérification. *Attention : celui-ci a pu être placé dans les mails indésirables.*
- Se connecter
- Dans le menu, choisir : DDNS -\> S'INSCRIRE
- Renseigner le nom d'hôte désiré et cliquer sur `+Ajouter`
- Aller dans son compte pour modifier certains paramètres, notamment le fuseau horaire
## Modifications sur la box
- Quelques modifications sont à apporter au niveau de la box. Disposant d’une livebox de chez Orange, la marche à suivre que je donne se réfère à ce type de box ; mais elle est grosso modo la même chez les autres opérateurs.
- Entrer dans le menu de sa box
  - Dans un navigateur taper `192.168.1.1` (pour une livebox Orange)
  - A l’invite de commande taper le mot de passe de sa box
  - Ouvrir la fenêtre `Réseau` en sélectionnant la touche correspondante
- Modifier le `NAT/PAT`
  - Aller à l’onglet `NAT/PAT`
  - A noter que si vous avez modifié le port externe SSH de votre raspberry, vous devez voir apparaître la règle correspondante de redirection de port
  - Remplissez la ligne saisissable 
  - La première colonne est libre, choisissez `Secure Web Serveur` ou `nouveau`
  - Pour le port interne, saisissez 80 qui est le port par défaut de Apache
  - Pour le port externe, saisissez 80
  - Laissez le protocole à `TCP`
  - Équipement : choisissez le nom de la raspberry ou saisissez son adresse IP locale.
  - Validez avec le bouton `Créer`
- Modifier le DynDNS
  - Allez à l’onglet DynDNS
  - Remplissez la ligne saisissable
  - Service : choisir son fournisseur : No-IP ou GnuDIP selon votre choix (c'est cette liste qui est limitative et ne propose que quelques fournisseurs)
  - Nom d’hôte/de domaine : mettre le nom de domaine attribué par le fournisseur
  - Email utilisateur : l’adresse mail avec laquelle vous vous êtes inscrit chez le fournisseur
  - Mot de Passe : votre mot de passe chez le fournisseur(et non pas celui du mail, bien sûr)
  - Validez avec le bouton « Enregistrer »
## Modifier le fichier de configuration Apache
- Ouvrir le fichier
    ```sh  
    sudo nano /etc/apache2/sites-available/project-camera.conf
    ```
- Commentez ou supprimez la ligne
    ```sh
    ServerName <IP locale de la Raspberry>
    ```
	(par exemple `192.168.1.49`)
- A la place copiez les deux lignes suivantes
    ```sh
    ServerName	<nom du site> 
    ServerAlias	www.<nom du site>
    ```
	Si votre site s'appelle monprojet.sytes.net, par exemple, les deux lignes seront
    ```sh
    ServerName	monprojet.sytes.net 
    ServerAlias	www.monprojet.sytes.net
    ```
- A la fin du fichier, avant la balise fermante `</VirtualHost>` copier les lignes suivantes : 
    ```sh
      ProxyPass /Rp1 http://<local IP Raspbery>:8081/
      ProxyPassReverse /Rp1 http://<local IP Raspbery>:8081/
      ProxyPass /Rp2 http://<local IP Raspbery>:8082/
      ProxyPassReverse /Rp2 http://<local IP Raspbery>:8082/
      ProxyPass /Rpi http://<local IP Raspbery>:8084/
      ProxyPassReverse /Rpi http://<local IP Raspbery>:8084/
    ```
	En remplaçant \<local IP Raspberry\> par l'IP locale de votre Raspberry.  
	Si vous avez choisi des valeurs autres que `8081`, `8082` et `8084` pour les ports mjpg-streamer des caméras, vous devez les modifier en conséquence.  
	De même si vous avec pris d'autes valeurs pour les clés `proxy` de la section `[hosts]` du fichier de configuration, vous devez également les modifier.  
	Vos lignes doivent ressembler à ceci
    ```sh
      ProxyPass /Rp1 http://192.168.1.49:8081/
      ProxyPassReverse /Rp1 http://192.168.1.49:8081/
      ProxyPass /Rp2 http://192.168.1.49:8082/
      ProxyPassReverse /Rp2 http://192.168.1.49:8082/
      ProxyPass /Rpi http://192.168.1.49:8084/
      ProxyPassReverse /Rpi http://192.168.1.49:8084/
     ```
 
	A modifier en fonction des ports mjpg-streamer que vous avez attribués aux différentes caméras et en fonction de l’adresse IP locale de votre raspberry.
- Le contenu du fichier doit être semblable à celui du fichier `project-camera.conf V3` disponible [ici]({{< ref "/script/project-camera_conf_V3.md" >}} "project-camera.conf V3")
## Modifier le fichier de configuration de Django
- Ouvrir le fichier
    ```sh 
    nano ~/folder/project/project/settings.py
    ```
- Ajoute le site dans ALLOWED_HOSTS
    ```python
    ALLOWED_HOSTS = ['<IP locale de la Raspberry>',
                  '<nom du site>’,
                  ]
    ``` 
	Par exemple :
    ```python
    ALLOWED_HOSTS = ['192.168.1.49',
                  'monprojet.sytes.net',
                  ]
    ```
## Mode Proxy et fichier views<span></span>.py
- Pour accéder au flux de mjpg-streamer depuis l’extérieur, il faut activer le module proxy de Apache et modifier le fichier views.py
- Ouvrir le fichier views.py
    ```sh
    nano ~/folder/project/camera/views.py
    ```
- Modifier les différentes fonctions stream en remplaçant 
    ```python
    "http://{}:{}/?action=stream".format(raspIP, cam_1_port)
    "http://{}:{}/?action=stream".format(raspIP, cam_2_port)
    "http://{}:{}/?action=stream".format(raspIP, cam_py_port)
    ```
      par :
    ```python
    "/{}?action=stream".format(Rp1)
    "/{}?action=stream".format(Rp2)
    "/{}?action=stream".format(Rpi)
    ```
- Ajouter en haut du fichier, au niveau de la déclaration des variables du parser du fichier de configuration, les variables `RP1`, `RP2` et `RPi`
    ```python
    Rp1 = parser.get("hosts", "proxy_1")
    Rp2 = parser.get("hosts", "proxy_2")
    Rpi = parser.get("hosts", "proxy_py")
    ```
- Le contenu du fichier doit être semblable à celui du fichier `views.py V2` disponible [ici]({{< ref "/script/views_py_V2.md" >}} "views.py V2").
- Activer le module proxy_http
    ```
    sudo a2enmod proxy_http
    ```
- Redémarrer Apache pour prendre en compte les changements
    ```
    sudo systemctl restart apache2
    ```
## Accès au site
### Si tout se passe bien
- L'accès au site se fait depuis la barre d'adresse d'un navigateur en tapant
    ```sh
    <nom du site>/camera
    ```
- par exemple, si votre site s'appelle monproject.sytes.net :
    ```sh
    monprojet.sytes.net/camera
    ```
- Vous pouvez vérifier que même en dehors du réseau local vous avez accès au site.
### Si vous n'avez pas d'accès au site depuis le réseau local
- Il est possible que vous ayiez accès au site depuis l'extérieur (par exemple depuis un téléphone portable dont la wifi a été coupée), mais pas depuis un appareil qui est sur le réseau local. Cela peut être dû, entre autre, à des problèmes d’autorisations et de paramétrages de la box.
- Solution risquée à proscrire : modifier la `DMZ`
  - Sauf si vous savez exactement ce que vous faites, il est déconseillé de modifier la `DMZ` au niveau de la box.
  - Entrer dans les paramètres `Réseau` de la box
  - Cliquer sur l’onglet `DMZ`
  - Intégrer la raspberry comme équipement de la `DMZ`
  - La connexion au site se fera depuis le réseau local avec la même commande `<nom du site>/camera`
- Solution moins élégante mais efficace et plus sûre
  - faire une copie du fichier /etc/apache2/ports.conf
    ```sh  
    sudo cp /etc/apache2/ports.conf /etc/apache2/ports.confORIGINAL
    ```
  - ouvrir le fichier en écriture
    ```sh
    sudo nano /etc/apache2/ports.conf 
    ```
  - ajouter un port (mettre un port peu utilisé, par exemple 54321) en ajoutant une ligne
    ```sh   
    Listen 54321
    ```
  - ouvrir le fichier /etc/apache2/sites-available/project-camera.conf
    ```sh
    sudo nano /etc/apache2/sites-available/project-camera.conf
    ```
  - ajouter un `<VirtualHost *:54321>` identique au `<VirtualHost *:80>`, à la différence près que le `ServerName` sera l'`IP locale de la Raspberry`.
  - le fichier doit être semblable au fichier `project-camera.conf V4` disponible [ici]({{< ref "/script/project-camera_conf_V4.md" >}} "project-camera.conf V4").
  - l’accès depuis un appareil local se fait en tapant dans un navigateur :
    ```sh
    <adresse IP locale Raspberry>:<port apache>/camera
    ```
      par exemple : 192.168.1.49:54321/camera
## A ce stade - Prochaine étape
### A ce stade
- Vous disposez d’un nom de site
- Votre site web est accessible depuis l’extérieur du réseau
- Il n’est pas https : vos données ne sont pas cryptées et peuvent donc être interceptées par des personnes mal intentionnées.
### Prochaine étape
- Sécuriser la connexion en https

