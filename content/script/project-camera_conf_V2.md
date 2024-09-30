---
title: "project-camera.conf V2"
date: 2021-01-24T20:20:54+01:00
draft: false
---

```sh
#mis en dehors du virtual host voir https://stackoverflow.com/questions/47803081/certbot-apache-error-name-duplicates-previous-wsgi-daemon-definition 

WSGIDaemonProcess project-camera.com python-home=/home/pi/folder/folder_venv python-path=/home/pi/folder/project

<VirtualHost *:80>

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
<Location "/">
AuthType Basic
AuthName "Authentification obligatoire"
AuthUserFile "/etc/apache2/.htpasswd"
Require valid-user
</Location>

</VirtualHost>

# Pour éliminer erreur AH00558
ServerName 127.0.0.1
```
