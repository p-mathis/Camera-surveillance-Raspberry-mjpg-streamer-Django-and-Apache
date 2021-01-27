---
title: "project-camera.conf V3"
date: 2021-01-24T23:14:04+01:00
draft: false
---

```sh
#mis en dehors du virtual host voir https://stackoverflow.com/questions/47803081/certbot-apache-error-name-duplicates-previous-wsgi-daemon-definition 

WSGIDaemonProcess project-camera.com python-home=/home/pi/folder/folder_venv python-path=/home/pi/folder/project

<VirtualHost *:80>

#!!!REMPLACER <site name> par le nom de votre site (par exemple, monprojet.sytes.net)
ServerName <site name>
ServerAlias www.<site name>

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

</VirtualHost>

# Pour éliminer erreur AH00558
ServerName 127.0.0.1
```
