---
title: "Fonction&nbsp;*jour*"
date: 2023-11-29T15:14:05+01:00
draft: false
---

## Position du problème
- Les photos affichées par la fonction `historique` de `views.py` incluent les photos nocturnes, même si la caméra n'est pas infrarouge
- On souhaite, ici, disposer des photos prises par les caméras diurnes pendant la durée du jour, sur une période couvrant 24 heures
## Schéma de la procédure
- Modifier le fichier `views.py` en créant une fonction `jour`
- Ajouter l'url `jour` dans le fichier `urls.py`
- Créer le fichier html `jour.html` qui permettra de visualiser les images
- On ne crée pas de bouton d'accès : la page sera affichée depuis la barre du navigateur à l'adresse `<monsite>/camera/jour/`
## Procédure
### Généralités
- On utilise, à peu de choses près, la même procédure que dans le tutoriel `partie 9`
- On va afficher les photos de n minutes avant le lever du soleil jusqu'à n minutes après le coucher
- Par défaut, on va définir la valeur `n` à 30 minutes dans le fichier `configuration.ini`
### Modifier le fichier&nbsp;*/etc/camera/configuration.ini*
#### Ouvrir le fichier en écriture
```sh
sudo nano ~/etc/camera/configuration.ini
```
#### Ajouter la variable&nbsp;*deltaSetRise*
- Dans `[locate]` (par exemple) ajouter la variable `deltaSetRise`
- Cette valeur donnera en minutes le temps de sélection des photos avant le lever du soleil et après le coucher
- Par défaut, la valeur est à 30
```sh
[locate]
////
deltaSetRise=30
```
### Modifier le fichier&nbsp;*views.py*
#### Ajouter la variable `deltaSetRise`
- Au niveau de la déclaration des différentes variables, déclarer `deltaSetRise`
```sh
deltaSetRise = parser.get("locate", "deltaSetRise")
```
#### Déclarer un `Q object`
- Les`Q objects` permettent des opérations sur les bases de données
- Au niveau des premières lignes du fichier `views.py`, appeler `Q`
```sh
from django.db.models import Q
```
#### Créer la fonction&nbsp;*jour*
- Cette fonction est écrite pour 4 caméras de jour, appelées *Appareil 1, 2, 4 et 5*
- Au niveau du fichier `views.py`, ajouter la fonction suivante 
```python
def jour(request):
    """Fonction qui sélectionne les photos des caméras de jour de x minutes avant le lever du soleil à x minutes après le coucher du soleil
    On rassemble les photos pour couvrir un nycthémère
    On crée autant de listes qu'il y a de caméras de jour
    Ici, on a 4 caméras de jour qui sont répertoriées dans la base de données par les identifiants 1, 2, 4, 5
    ADAPTER CES IDENTIFIAANTS AUX NUMEROS DE CAMERA ET A LEUR NOMBRE"""

    lieu = SunTimes(longitude, latitude, altitude)
    maintenant = local_tz.localize(datetime.now())     #voir http://pytz.sourceforge.net/
    lever = lieu.riselocal(maintenant)
    coucher = lieu.setlocal(maintenant)
    coucherHier = lieu.setlocal(maintenant - timedelta(1))
    leverHier = lieu.riselocal(maintenant - timedelta(1))
    leverDelta = lever - timedelta(minutes=deltaSetRise)       # par ex 30 minutes avant lever soleil
    coucherDelta = coucher + timedelta(minutes=deltaSetRise)    # par ex 30 minuts après coucher soleil
    coucherDeltaHier = coucherHier + timedelta(minutes=deltaSetRise)
    leverDeltaHier = leverHier - timedelta(minutes=deltaSetRise)
    maintenantHier= maintenant - timedelta(1)

    if leverDelta <= maintenant <= coucherDelta:
        #On est en journée ; on sélectionne les photos allant du lever à maintenant. On sélectionne aussi les photos allant de maintenant - 24 heures à coucher hier
        jour_photo_list_1 = Photo.objects.filter(appareil=1).filter(Q(date__gt=leverDelta, date__lt=maintenant) | Q(date__gt=maintenantHier, date__lt=coucherDeltaHier)).order_by('-date')
        jour_photo_list_2 = Photo.objects.filter(appareil=2).filter(Q(date__gt=leverDelta, date__lt=maintenant) | Q(date__gt=maintenantHier, date__lt=coucherDeltaHier)).order_by('-date')       
        jour_photo_list_4 = Photo.objects.filter(appareil=4).filter(Q(date__gt=leverDelta, date__lt=maintenant) | Q(date__gt=maintenantHier, date__lt=coucherDeltaHier)).order_by('-date')        
        jour_photo_list_5 = Photo.objects.filter(appareil=5).filter(Q(date__gt=leverDelta, date__lt=maintenant) | Q(date__gt=maintenantHier, date__lt=coucherDeltaHier)).order_by('-date')
                        
    elif leverDelta > maintenant:
        # On est la nuit mais après minuit: on selectionne les photos allant du jour précédent du matin au soir
        jour_photo_list_1 = Photo.objects.filter(appareil=1).filter(date__gt=leverDeltaHier, date__lt=coucherDeltaHier).order_by('-date')
        jour_photo_list_2 = Photo.objects.filter(appareil=2).filter(date__gt=leverDeltaHier, date__lt=coucherDeltaHier).order_by('-date')
        jour_photo_list_4= Photo.objects.filter(appareil=4).filter(date__gt=leverDeltaHier, date__lt=coucherDeltaHier).order_by('-date')
        jour_photo_list_5= Photo.objects.filter(appareil=5).filter(date__gt=leverDeltaHier, date__lt=coucherDeltaHier).order_by('-date')
    else:
        # On est la nuit mais avant minuit : on selectionne les photos du même jour allant du matin au soir
        jour_photo_list_1 = Photo.objects.filter(appareil=1).filter(date__gt=leverDelta, date__lt=coucherDelta).order_by('-date')
        jour_photo_list_2 = Photo.objects.filter(appareil=2).filter(date__gt=leverDelta, date__lt=coucherDelta).order_by('-date')
        jour_photo_list_4 = Photo.objects.filter(appareil=4).filter(date__gt=leverDelta, date__lt=coucherDelta).order_by('-date')
        jour_photo_list_5 = Photo.objects.filter(appareil=5).filter(date__gt=leverDelta, date__lt=coucherDelta).order_by('-date')

    min_length = min(len(jour_photo_list_1), len(
        jour_photo_list_2), len(jour_photo_list_4), len(jour_photo_list_5))

    jour_photo_list_group = []
    for i in range(min_length):
        new_group = [jour_photo_list_1[i], jour_photo_list_2[i], jour_photo_list_4[i], jour_photo_list_5[i]] 
        jour_photo_list_group.extend(new_group)

    context = {
        'jour_photo_list_group': jour_photo_list_group,
    }

    return render(request, "{}/jour.html".format(appli), context)

```
- Toutes les photos vont s'afficher selon le critère temporel choisi
- Si on souhaite n'afficher qu'une photo sur N (par exemple, une photo toutes les trois minutes), il faut, comme dans les fonctions `historique` et `nuit` sélectionner une photo toutes les N photos dans les listes de photos
### Modifier le fichier&nbsp;*folder/project/camera/urls.py*
- Ouvrir le fichier en écriture
- Au niveau de la liste `urlpatterns` ajouter
```sh
path('jour/', views.jour, name="jour"),
```
- *Bien respecter les virgules dans la liste*
### Ecrire le fichier&nbsp;*jour.html*
#### Créer le fichier en écriture
```sh
nano ~/folder/project/camera/templates/camera/jour.html
```
#### Coller dans le fichier le contenu suivant
```html
{% extends "camera/base.html" %}
{% load static %}

{% block header %}
<h1 class="monh1">Photos de Jour</h1>

{% endblock %}

{% block content %}


<table>
  <tr>
  {% for photo in jour_photo_list_group %}
      <td>
        <a href="{% static photo.file_photo_jpg %}">
        <img class="centre-image imgresponsive" src="{% static photo.file_photo_jpg %}" height="150" width="225" alt="photo non disponible" loading="lazy" /><figcaption>{{photo.name}} - {{photo.appareil}}</figcaption>
        </a>
      </td>
 {% if forloop.last %}
   </tr>
 {% else %}
   {% if forloop.counter|divisibleby:"4" %}
     </tr><tr>
   {% endif %}
 {% endif %}
{% endfor %}
</table>

{% endblock %}

```
## Résultat
- Redémarrer la `raspberry`
- Les images sont visibles à l'adresse `<monsite>/camera/jour/`
- Si on le souhaite, il est possible d'ajouter des boutons d'accès direct à la page