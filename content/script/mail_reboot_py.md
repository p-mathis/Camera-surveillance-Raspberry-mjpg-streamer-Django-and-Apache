---
title: "mail_reboot.py"
date: 2021-01-25T11:03:46+01:00
draft: false
---
```python
#!/usr/bin/python3
# -*-coding:Utf-8

import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from time import sleep
from configparser import ConfigParser

parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

mail_site = parser.get("mails", "mail_site")
mail_site_mdp = parser.get("mails", "mail_site_mdp")
mail_perso = parser.get("mails", "mail_perso")
smtp_port = int(parser.get("mails", "smtp_port"))
delay_send_mail_reboot=int(parser.get("frequences", "delay_send_mail_reboot"))

fournisseur = mail_site.split("@")[1]
login = mail_site.split("@")[0]

sleep(delay_send_mail_reboot)
date = datetime.datetime.now()
dateString = date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
server=smtplib.SMTP("smtp.{}".format(fournisseur),smtp_port)
server.ehlo()
server.starttls()
server.login(login,mail_site_mdp)
msg = MIMEMultipart()
fromaddr = mail_site
msg['From'] = fromaddr
msg['Subject'] = f'Redémarrage de la raspberry Camera - {dateString}'
body = f'ATTENTION : la raspberry a redémarré le {dateString}.\nVérifiez le bon fonctionnement des caméras.'
msg.attach(MIMEText(body, 'plain'))
server.sendmail(fromaddr, mail_perso, msg.as_string())
```
