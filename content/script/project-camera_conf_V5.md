---
title: "project-camera.conf V5"
date: 2021-01-25T10:04:57+01:00
draft: false
---

```sh
#mis en dehors du virtual host voir https://stackoverflow.com/questions/47803081/certbot-apache-error-name-duplicates-previous-wsgi-daemon-definition 
WSGIDaemonProcess project-camera.com python-home=/home/pi/folder/folder_venv python-path=/home/pi/folder/project

<VirtualHost *:80>

#!!!REMPLACER <site name> par le nom de votre site (par exemple, monprojet.sytes.net)
ServerName <site name>
ServerAlias www.<site name>

Redirect permanent / https://<site name>

</VirtualHost>

<VirtualHost *:443>

#!!!REMPLACER <site name> par le nom de votre site (par exemple, monprojet.sytes.net)
ServerName <site name>
ServerAlias <site name>

#pour accroître la sécurité et être en HSTS
Redirect permanent /secure https://<site name>

ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined

Alias /static/ /var/www/stock/

<Directory /var/www/stock>
Require all granted
</Directory>

<Directory /home/pi/folder/project/camera/static>
Require all granted
</Directory>

WSGIScriptAlias / /home/pi/folder/project/project/wsgi.py

WSGIProcessGroup project-camera.com

<Directory /home/pi/folder/project/project>
<Files wsgi.py>
Require all granted
</Files>
</Directory>

#pour forcer authentification accès site
<Location "/">
AuthType Basic
AuthName "Authentification obligatoire"
AuthUserFile "/etc/apache2/.htpasswd"
Require valid-user
</Location>

#Pour accéder aux flux depuis l'extérieur du réseau
#!!!REMPLACER <local IP Raspberry> par l'IP locale de votre Raspberry
# Si vous avez d'autres ports pour les caméras, modifiez les en conséquence

ProxyPass /Rp1 http://<local IP Raspberry>:8081/
ProxyPassReverse /Rp1 http://<local IP Raspberry>:8081/
ProxyPass /Rp2 http://<local IP Raspberry>:8082/
ProxyPassReverse /Rp_2 http://<local IP Raspberry>:8082/
ProxyPass /Rpi http://<local IP Raspberry>:8084/
ProxyPassReverse /Rpi http://<local IP Raspberry>:8084/

#Pour le certificat
#!!!REMPLACER <site name> par le nom de votre site (par exemple, monprojet.sytes.net)
SSLEngine on
SSLCertificateFile /etc/letsencrypt/live/<site name>/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/<site name>/privkey.pem

#Pour accroître la sécurité
SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
SSLHonorCipherOrder on
SSLCompression off
SSLCipherSuite ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-DSS-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384
SSLOptions +StrictRequire

Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains;"

</VirtualHost>

#Pour accès sur le réseau local

<VirtualHost *:54321>
#Nécessaire si la box ne permet pas de rediriger en interne les données du site 
#!!!REMPLACER <local IP Raspberry> par l’IP de la Raspberry ; par exemple : ServerName 192.168.1.49
ServerName <local IP Raspberry>

ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined

Alias /static/ /var/www/stock/

<Directory /var/www/stock>
Require all granted
</Directory>

<Directory /home/pi/folder/project/camera/static>
Require all granted
</Directory>

WSGIScriptAlias / /home/pi/folder/project/project/wsgi.py

WSGIProcessGroup project-camera.com

<Directory /home/pi/folder/project/project>
<Files wsgi.py>
Require all granted
</Files>
</Directory>

#pour forcer authentification accès site
<Location "/ ">
AuthType Basic
AuthName "Authentification obligatoire"
AuthUserFile "/etc/apache2/.htpasswd"
Require valid-user
</Location>

#Pour accéder aux flux depuis l'extérieur du réseau
#!!!REMPLACER <local IP Raspberry> par l'IP locale de votre Raspberry
# Si vous avez d'autres ports pour les caméras, modifiez les en conséquence

ProxyPass /Rp1 http://<local IP Raspberry>:8081/
ProxyPassReverse /Rp1 http://<local IP Raspberry>:8081/
ProxyPass /Rp2 http://<local IP Raspberry>:8082/
ProxyPassReverse /Rp_2 http://<local IP Raspberry>:8082/
ProxyPass /Rpi http://<local IP Raspberry>:8084/
ProxyPassReverse /Rpi http://<local IP Raspberry>:8084/

</VirtualHost>

#ajouté pour éliminer erreur AH00558
ServerName 127.0.0.1
```
