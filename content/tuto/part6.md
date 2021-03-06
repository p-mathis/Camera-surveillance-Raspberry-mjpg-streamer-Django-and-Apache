---
title: "Tutoriel : Partie 6 - Sécuriser le site en https"
date: 2021-01-25T09:19:23+01:00
draft: false
---

## A faire
- Installer Certbot et obtenir un certificat
- Modifier le fichier de configuration du site
- Modifier le `NAT/PAT`au niveau de la box
- Tester la sécurité du site
- Renouveler automatiquement le certificat
## Comment sécuriser un site ?
- Il est possible de sécuriser un site en utilisant les services de Cloudflare. Mais dans la mesure où on utilise un Dyn DNS (No-IP), la procédure est plutôt complexe, nécessitant par exemple de passer par DNS-O-Matic.
- Il est finalement plus simple d’utiliser Certbot, d’autant que l’on peut automatiser le renouvellement des certificats. La manière la plus simple d’installer certbot est d’utiliser la commande snap.
## Sources
- [memoinfo](https://www.memoinfo.fr/tutoriels-linux/configurer-lets-encrypt-apache/)
- [certbot](https://certbot.eff.org/lets-encrypt/snap-apache.html)
## Activer les modules de Apache
- Activer le module ssl
    ```sh
    sudo a2enmod ssl
    ```
- Activer le module rewrite
    ```sh
    sudo a2enmod rewrite
    ```
- Prendre en compte les modifications
    ```sh
    sudo systemctl restart apache2
    ```
## Installer Certbot et obtenir un certificat
### Installer Snapd
- La manière la plus simple d'installer Certbot est de passer par la commande snap
- Installer snapd
    ```sh
    sudo apt install snapd
    ```
A l’invite de commande, taper O (oui)
- Rebouter le système
    ```sh
    sudo reboot
    ```
- Tester snap
    ```sh
    sudo snap install hello-world
    ```
	doit vous renvoyer : `hello-world 6.4 from Canonical✓ installed`
- Installer core
    ```sh
    sudo snap install core
    ```
### Installer Certbot
- Installer Certbot
    ```sh
    sudo snap install --classic certbot
    ```
- Créer un lien symbolique de /snap/bin/certbot vers /usr/bin/certbot
    ```sh
    sudo ln -s /snap/bin/certbot /usr/bin/certbot
    ```
### Installer le certificat Certbot
- On peut laisser Certbot installer le certificat et modifier lui-même les fichiers Apache. Il est préférable d’installer le certificat mais de modifier soi-même les fichiers de configuration du site, notamment pour pouvoir maîtriser certains paramètres de sécurité.
- Lancer la commande
    ```sh  
    sudo certbot certonly --apache --rsa-key-size 4096
    ```
	On a fixé la taille de la clé RSA à 4096 bit contre 2048 par défaut.
- Répondre aux invites de commandes
  - Entrer (ou non) son adresse mail.
  - Read the terms of service : accepter en tapant `Y` à l’invite de commande
  - Electronic Frontier Foundation : accepter ou non 
  - Quel nom activer pour le certificat : deux options
    - Soit rien n’est proposé : rentrer le nom du site (monsite.sytes.net par exemple)
    - Soit deux options sont proposées :
      - 1 :`<nom du site>` (`monsite.sytes.net` par exemple)
      - 2 :`www.<nom du site>` (`www.monsite.sytes.net` par exemple)  
      
	  Taper 1 car c’est le nom qui a été donné à No-IP.
## Modifier le fichier /etc/apache2/sites-available/project-camera.conf
- Ouvrir le fichier
    ```sh
    sudo nano /etc/apache2/sites-available/project-camera.conf
    ```
- Faire un `copier` du contenu du VirtualHost 80 (voir plus loin)
- Modifier le contenu de `<VirtualHost *:80>` (en remplaçant `<nom du site>`par le nom de votre site) comme indiqué ci-dessous
	```sh
    ServerName <nom du site>
    ServerAlias www.<nom du site>
    Redirect permanent / https://<nom du site>
    ```
- Créer le VirtualHost 443
    ```sh
    <VirtualHost *:443>
    ```
	    et sous cette ligne copier l’ancien contenu du VirtualHost80
- Ajouter les lignes concernant le certificat en remplaçant `<nom du site>`par le nom de votre site
    ```sh
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/<nom du site>/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/<nom du site>/privkey.pem
    ```
- Ajouter les lignes concernant la sécurité
    ```sh
    SSLProtocol -all +TLSv1.2 +TLSv1.3
    SSLHonorCipherOrder on
    SSLCompression off
    SSLCipherSuite ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-DSS-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384
    SSLOptions +StrictRequire
    ```
- Forcer le STS
    ```sh 
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains;"
    ```
- Balise de fermeture du VirtualHost 
    ```sh
    </VirtualHost>
    ```
- Le contenu du fichier doit être semblable à celui du fichier `project-camera.conf V5` disponible [ici]({{< ref "/script/project-camera_conf_V5.md" >}} "project-camera.conf V5")
- Si vous copiez/collez le contenu de ce fichier, vous devrez modifier l’IP locale, le nom du site, les ports des caméras… en fonction de vos paramètres.
### Explications sur ces commandes
- `SSLEngine on` : Activation du module `SSL`
- `SSLCertificateKeyFile` : chemin vers le fichier `privkey.pem`
- `SSLCertificateChainFile` : chemin vers le fichier `chain.pem`
- `SSLProtocol` : N’active que les versions les plus sûres : `TLSv1.2` et `TLSv1.3`
- `SSLHonorCipherOrder` : Quand activé, le serveur force ses préférences de protocoles et non le navigateur du client.
- `SSLCompression` : La compression SSL n’est pas activée
- `SSLOptions +StrictRequire` : Exige une connexion SSL stricte
- `SSLCipherSuite` : Liste des algorithmes de chiffrement disponibles
- `Header always set Strict-Transport-Security `: ou `HSTS`. Indique aux navigateurs que seul le https est supporté. 
## Modifications au niveau de la box
- Entrer dans la box en tapant `192.168.1.1` dans la barre d'adresse du navigateur (à modifier selon l'opérateur et le réseau)
- Ajouter la règle dans le `NAT/PAT`
  - `Application Service` : donner un nouveau nom, par exemple Web Server https
  - `Port interne` : 443
  - `Port externe` : 443
  - `Protocole` : TCP
  - `Equipement` : votre raspberry
  - `IP externe` : toutes, sauf si vous voulez limiter l’accès
## Tester la sécurité
- En accédant au site depuis l'extérieur du réseau, vous constatez que le symbole cadenas précède l'adresse de votre site.
- Tester le niveau de sécurité
  - Aller sur le site de [SSL Labs](https://www.ssllabs.com/ssltest/)
  - Entrez le nom de votre site pour le tester
  - Théoriquement vous devez obtenir la note `A+`
## Renouveler automatiquement le certificat certbot
- Le certificat est valable 90 jours ; on écrit un script bash pour le renouveler automatiquement.
- Créer le script et l'ouvrir en écriture
    ```sh
    nano ~/script/certbotRenew.sh
    ```
- Écrire le script en ajoutant les deux lignes
    ```sh
    #!bin/bash
    sudo certbot renew --force-renewal
    ```
- Éditer le crontab
    ```sh
    crontab -e
    ```
- Lancer le script tous les deux mois en ajoutant la ligne
    ```sh
    10 02 3 */2 * sh /home/pi/script/certbotRenew.sh
    ```
	Le script sera lancé à 2 heures 10 le troisième jour des mois pairs. Dans la mesure où certains trimestres durent 92 jours, on doit renouveler le certificat tous les deux mois.
## A ce stade - Prochaine étape
### A ce stade
- Votre site est sécurisé https
- Il a un score global A+
- Le certificat de Let’s Encrypt est renouvelé automatiquement tous les deux mois.
### Etape suivante
- Automatiser les mises à jour de la raspberry
- Être informé des redémarrages de la raspberry
- Etre informé des changements d’IP de la box
- Mettre en place un accès par ssh sur la raspberry depuis son téléphone portable


