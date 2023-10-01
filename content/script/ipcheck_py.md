---
title: "ipcheck.py"
date: 2021-01-25T14:47:05+01:00
draft: false
---

```python
#!/usr/bin/python3.5
# -*-coding:Utf-8

import json
import requests
import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from configparser import ConfigParser

parser_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(parser_file)

mail_site = parser.get("mails", "mail_site")
mail_site_mdp = parser.get("mails", "mail_site_mdp")
mail_perso = parser.get("mails", "mail_perso")
smtp_port = int(parser.get("mails", "smtp_port"))
home = parser.get("paths", "home")

fournisseur = mail_site.split("@")[1]
login =  mail_site.split("@")[0]
filePath = f'{home}/currentIP.txt'

def notifyByMail(ip, date):
	print("Sending email...")
	dateString = date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
	server=smtplib.SMTP(f'smtp.{fournisseur}',smtp_port)
	server.ehlo()
        server.starttls()
	server.login(login,mail_site_mdp)
	msg = MIMEMultipart()
	fromaddr = mail_site
	msg['From'] = fromaddr
	msg['Subject'] = f'IP Raspberry Caméras - {ip}'
	msg.attach(MIMEText(body, 'plain'))
	server.sendmail(fromaddr,mail_perso ,msg.as_string())
	print("Sent")

def getPreviousIP():
	try:
		fichierIP = open(filePath,"r")
		rebuilt = json.loads(fichierIP.read())
		return rebuilt["ip"]
	except FileNotFoundError:
		return "-1"

def saveIP(ip, date):
	dateString = date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
	values = {"ip":ip, "date":dateString}
	text = json.dumps(values)
	fichierIP = open(filePath,"w")
	fichierIP.write(text)
	fichierIP.close()

ip = json.loads(requests.get("http://httpbin.org/ip").text)["origin"]

if getPreviousIP() != ip:
	date = datetime.datetime.now()
	saveIP(ip, date)
	notifyByMail(ip, date)
```
