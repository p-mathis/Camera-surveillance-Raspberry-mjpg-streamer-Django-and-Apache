---
title: "views.py V2"
date: 2021-01-24T23:28:16+01:00
draft: false
---

```python
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from datetime import datetime, timedelta
from django.utils import timezone
import pytz         #pour régler les problèmes d'heure naïve et consciente
from pytz import timezone
from suntimes import SunTimes
from configparser import ConfigParser

from .models import Photo, Appareil

config_file = "/etc/camera/configuration.ini"
parser = ConfigParser()
parser.read(config_file)

longitude = float(parser.get("locate", "longitude"))
latitude = float(parser.get("locate", "latitude"))
altitude = float(parser.get("locate", "altitude"))
zone = parser.get("locate", "zone")

hz_historique = int(parser.get("frequences", "historique"))
hz_nuit = int(parser.get("frequences", "nuit"))
hz_capture = int(parser.get("frequences", "capture"))

raspIP = parser.get("hosts", "raspIP")
cam_1_port = parser.get("camera", "cam_1_port")
cam_2_port = parser.get("camera", "cam_2_port")
cam_py_port = parser.get("camera", "cam_py_port")

Rp1 = parser.get("hosts", "proxy_1")
Rp2 = parser.get("hosts", "proxy_2")
Rpi = parser.get("hosts", "proxy_py")

display_nombre = int(float(parser.get("frequences", "display_jour")) * 3600 * 24 / hz_capture)

appli = parser.get("paths", "appli")

local_tz = timezone(zone)
utc = pytz.utc

def accueil(request):
    response = TemplateResponse(request, "{}/accueil.html".format(appli))
    return response

def historique(request):
    """On visionne les trois caméras sur les 24 dernière heures ; on prend une photo toutes les n minutes."""
    maintenant = local_tz.localize(datetime.now())     #voir http://pytz.sourceforge.net/

    latest_photo_list_1 = Photo.objects.filter(appareil=1).order_by('-date')[:display_nombre]
    latest_photo_list_2 = Photo.objects.filter(appareil=2).order_by('-date')[:display_nombre]
    latest_photo_list_py = Photo.objects.filter(appareil=3).order_by('-date')[:display_nombre]
    
    latest_photo_list_1_oneoutofN = []
    latest_photo_list_2_oneoutofN = []
    latest_photo_list_py_oneoutofN = []

    for photo in latest_photo_list_1:      #pour ne sélectionner qu'une photo sur N
        if (photo.date - maintenant).seconds // hz_capture % hz_historique == 0:        
            latest_photo_list_1_oneoutofN.append(photo)

    for photo in latest_photo_list_2:      #pour ne sélectionner qu'une photo sur N
        if (photo.date - maintenant).seconds // hz_capture % hz_historique == 0:
            latest_photo_list_2_oneoutofN.append(photo)

    for photo in latest_photo_list_py:      #pour ne sélectionner qu'une photo sur N
        if (photo.date - maintenant).seconds // hz_capture % hz_historique == 0:
            latest_photo_list_py_oneoutofN.append(photo)

    min_length = min(len(latest_photo_list_1_oneoutofN), len(latest_photo_list_2_oneoutofN), len(latest_photo_list_py_oneoutofN))

    latest_photo_list_group3 = []  #groupe les photos par trois (une par caméra)
    for i in range(min_length):
        new_group = [latest_photo_list_1_oneoutofN[i], latest_photo_list_2_oneoutofN[i], latest_photo_list_py_oneoutofN[i]] 
        latest_photo_list_group3.extend(new_group)

    context = {
        'latest_photo_list_group3': latest_photo_list_group3,
    }

    return render(request, "{}/historique.html".format(appli), context)

def nuit(request):
    
    #lieu = SunTimes(longitude, latitude, altitude, zone)
    lieu = SunTimes(longitude, latitude, altitude)
    maintenant = local_tz.localize(datetime.now())     #voir http://pytz.sourceforge.net/
    lever = lieu.dateRiseLocal(maintenant)
    coucher = lieu.dateSetLocal(maintenant)
    coucherHier = lieu.dateSetLocal(maintenant - timedelta(1))
    leverDemain = lieu.dateRiseLocal(maintenant + timedelta(1))

    if lever <= maintenant <= coucher:
        #on est en journée ; on sélectionne les photos allant du coucher de la veille au lever de ce jour
        night_photo_list = Photo.objects.filter(appareil=3).filter(date__gt=coucherHier, date__lt=lever).order_by('-date')
        horaire = [lever.strftime('%Hh %Mmn'), lever.day, lever.month, coucherHier.strftime('%Hh %Mmn'), coucherHier.day, coucherHier.month]

    elif maintenant < lever:
        #On est après minuit, mais avant le lever. On sélectionne les photos de coucherHier à maintenant
        night_photo_list = Photo.objects.filter(appareil=3).filter(date__gt=coucherHier).order_by('-date')
        horaire = [lever.strftime('%Hh %Mmn'), lever.day, lever.month, coucherHier.strftime('%Hh %Mmn'), coucherHier.day, coucherHier.month]
    else:
        #on est avant minuit mais après le coucher. On sélectionne les photos de coucher à maintenant
        night_photo_list = Photo.objects.filter(appareil=3).filter(date__gt=coucher).order_by('-date')
        horaire = [leverDemain.strftime('%Hh %Mmn'), leverDemain.day, leverDemain.month, coucher.strftime('%Hh %Mmn'), coucher.day, coucher.month]    
    
    night_photo_list_oneoutofN = []
    for photo in night_photo_list:      #pour ne sélectionner qu'une photo sur N
        if (maintenant - photo.date).seconds // hz_capture % hz_nuit == 0:
            night_photo_list_oneoutofN.append(photo)
    
    context = {
        'night_photo_list_oneoutofN': night_photo_list_oneoutofN,
        'horaire': horaire
    }

    return render(request, "{}/nuit.html".format(appli), context)

def parheure(request):
    """On visionne les trois caméras sur les 24 dernière heures ; la pagination se fera heure par heure."""

    latest_photo_list_1 = Photo.objects.filter(appareil=1).order_by('-date')[:display_nombre]
    latest_photo_list_2 = Photo.objects.filter(appareil=2).order_by('-date')[:display_nombre]
    latest_photo_list_py = Photo.objects.filter(appareil=3).order_by('-date')[:display_nombre]

    min_length = min(len(latest_photo_list_1), len(latest_photo_list_2), len(latest_photo_list_py))

    latest_photo_list_group3 = []
    for i in range(min_length):
        new_group = [latest_photo_list_1[i], latest_photo_list_2[i], latest_photo_list_py[i]] 
        latest_photo_list_group3.extend(new_group)

    paginator = Paginator(latest_photo_list_group3, 180)
    page = request.GET.get('page')
    photos = paginator.get_page(page)

    context = {
        'photos': photos,
    }

    return render(request, "{}/parHeure.html".format(appli), context)

def stream_py(request):
    stream = ["/{}?action=stream".format(Rpi)]
    context = {
        'stream': stream,
    }

    return render(request, "{}/stream_py.html".format(appli), context)

def stream_1(request):
    stream = ["/{}?action=stream".format(Rp1)]
    context = {
        'stream': stream,
    }

    return render(request, "{}/stream_1.html".format(appli), context)


def stream_2(request):
    stream = ["/{}?action=stream".format(Rp2)]    
    context = {
        'stream': stream,
    }

    return render(request, "{}/stream_2.html".format(appli), context)

def stream_AllCam(request):
    stream = ["/{}?action=stream".format(Rp1),"/{}?action=stream".format(Rp2), "/{}?action=stream".format(Rpi) ]
    context = {
        'stream': stream,
    }

    return render(request, "{}/stream_AllCam.html".format(appli), context)
```
