---
title: "Présentation"
date: 2021-01-22T20:20:55+01:00
draft: false
---

## Introduction
Création d'un site internet hébergé sur une raspberry fonctionnant sous un serveur Apache. Le site est construit avec le cadre de développement (framework) Django. Les images et les flux vidéos de trois caméras sont capturés par mjpg-streamer.
## Objectif
Créer une surveillance à distance de chevaux en stabulation libre.
Les chevaux peuvent aller et venir hors d'un abri pour se rendre dans les prés avoisinants. La surveillance a pour but de savoir si les chevaux sont dans l’abri ou dans les prés et de vérifier que leur comportement y est normal. Mais également, lorsqu’ils sont hors de vue des caméras de savoir si dans un passé récent ils étaient bien présents.  
  
Le cahier des charges est le suivant :
- Disposer de trois caméras, dont une à vision nocturne.
- Chaque caméra doit assurer une vision en flux direct.
- Chaque caméra doit prendre des photos à intervalles réguliers. Il faut pouvoir consulter ces photos afin de savoir si dans un passé récent les chevaux étaient bien présents.
- Les informations doivent être disponibles depuis un navigateur web accessible localement et depuis l’extérieur du réseau.
## Les matériels
- Une Raspberry Pi, ici un modèle Pi3-B+ avec une carte micro-SD de 16 Giga relié au réseau local.
- Deux webcam en connexion USB.
- Une pi-caméra à vision nocturne.
- Un projecteur infra-rouge pour éclairer la zone de surveillance de la caméra nocturne.
- Un ordinateur.
## Résultat final
Le résultat sera de ce type :
- La page d'accueil
{{< figure src="/media/cam_accueil.png">}}
- Les trois caméras
{{< figure src="/media/cam_3cam.png">}}
- Une caméra
{{< figure src="/media/cam_cam1.png">}}
- La page Historique
{{< figure src="/media/cam_historique.png">}}
- La page Nuit
{{< figure src="/media/cam_nuit.png">}}
- La page par 24 heures
{{< figure src="/media/cam_24H.png">}}
## Guides d'installation
Deux guides d'installation sont disponibles :
- [Guide rapide]({{< ref "/rapid/rapid.md" >}} "Guide Rapide") : pour une mise en place rapide des scripts. Ce guide est peu détaillé.
- [Guide pas à pas]({{< ref "/tuto/part1.md" >}} "Guide Pas à Pas") : mise en place didactique des services permettant un bonne compréhension de la démarche.
  - installation de la raspberry
  - installation de mjpg-streamer
  - installation de Django et utilisation du serveur embarqué de Django
  - installation de Apache et de mod-wsgi : utilisation du serveur apache sur le réseau local
  - obtention d'un nom de domaine et utilisation du serveur apache sur le réseau extérieur
  - sécurisation https du site avec Certbot
  - mise en place de divers scripts facilitant la maintenance

