---
title: "Tutoriel : Partie 9 - Afficher les photos de nuit minutes par minutes"
date: 2023-10-21T12:02:17+02:00
draft: false
---

## Position du problème
- Les photos de nuit obtenues par la fonction `nuit` du fichier `views.py` ne sont pas toutes affichées
- Effectivement, seule une photo sur N est affichée, N étant la fréquence définie dans le fichier `configuration.ini` par la variable `[frequences] nuit`
- Si on souhaite disposer de toutes les photos de nuit, il faut mettre en place une nouvelle fonction
## Schéma de la procédure
- Modifier le fichier `views.py` en créant une fonction `nuitparminute`
- Ajouter l'url `nuitParMinute` dans le fichier `urls.py`
- Créer le fichier html `nuitParMinute.html` qui permettra de visualiser les images
- Créer un bouton pour la page `nuitParMinute` dans la page d'accueil
## Modifier le fichier `views.py`
### Ouvrir le fichier `views.py`en écriture
```sh
nano ~/folder/project/camera/views.py
```
### Ajouter la fonction `nuitparminute`
- A la fin du fichier ou bien après la fonction `def nuit(request)` si vous souhaitez que les fonctions soient rassemblées
- Ajouter la fonction suivante
```python
def nuitparminute(request):
        
    #lieu = SunTimes(longitude, latitude, altitude, zone)
    lieu = SunTimes(longitude, latitude, altitude)
    maintenant = local_tz.localize(datetime.now())     #voir http://pytz.sourceforge.net/
    lever = lieu.riselocal(maintenant)
    coucher = lieu.setlocal(maintenant)
    coucherHier = lieu.setlocal(maintenant - timedelta(1))
    leverDemain = lieu.riselocal(maintenant + timedelta(1))

    if lever <= maintenant <= coucher:
        #On est en journée ; on sélectionne les photos allant du coucher de la veille au lever de ce jour
        night_photo_list = Photo.objects.filter(appareil=3).filter(date__gt=coucherHier, date__lt=lever).order_by('-date')
        horaire = [lever.strftime('%Hh %Mmn'), lever.day, lever.month, coucherHier.strftime('%Hh %Mmn'), coucherHier.day, coucherHier.month]

    elif maintenant < lever:
        #On est après minuit, mais avant le lever. On sélectionne les photos de coucherHier à maintenant
        night_photo_list = Photo.objects.filter(appareil=3).filter(date__gt=coucherHier).order_by('-date')
        horaire = [lever.strftime('%Hh %Mmn'), lever.day, lever.month, coucherHier.strftime('%Hh %Mmn'), coucherHier.day, coucherHier.month]
    else:
        #On est avant minuit mais après le coucher. On sélectionne les photos de coucher à maintenant
        night_photo_list = Photo.objects.filter(appareil=3).filter(date__gt=coucher).order_by('-date')
        horaire = [leverDemain.strftime('%Hh %Mmn'), leverDemain.day, leverDemain.month, coucher.strftime('%Hh %Mmn'), coucher.day, coucher.month]    
    
    
    context = {
        'night_photo_list': night_photo_list,
        'horaire': horaire
    }

    return render(request, "{}/nuitParMinute.html".format(appli), context)

```
### Sauvegarder et fermer : 
```sh
Ctrl+O
Entrée
Ctrl+X
```
## Modifier le fichier `urls.py`
### Ouvrir le fichier `urls.py` en écriture
```sh
nano ~/folder/project/camera/urls.py
```
### Ajouter le path pour la fonction `nuitparminute`
- Aller à la fin de la liste `urlpatterns`
- Ajouter la ligne
```python
path('nuitParMinute/', views.nuitparminute, name="nuitParMinute")
```
- **Vérifier qu'il y a bien une virgule entre ce path et le path précédent**

### Sauvegarder et fermer
## Ecrire le fichier nuitParMinute.html
### Créer le fichier en écriture
```sh
nano ~/folder/project/camera/templates/camera/nuitParMinute.html
```
### Coller dans le fichier le contenu suivant
```html
{% extends "camera/base.html" %}
{% load static %}

{% block header %}
<h1 class="monh1">La nuit heure par heure</h1>
<pre>
  Coucher : {% if horaire %}{{ horaire.3 }} - le {{horaire.4}}/{{horaire.5}}{% endif %}
  Lever   : {% if horaire %}{{ horaire.0 }} - le {{horaire.1}}/{{horaire.2}}{% endif %}
  
  </pre>
{% endblock %}

{% block content %}

<table>
    <tr>
    {% for photo in night_photo_list %}
        <td>
          <a href="{% static photo.file_photo_jpg %}">
          <img class="centre-image imgresponsive" src="{% static photo.file_photo_jpg %}" height="150" width="225" alt="photo nocturne indisponible"/><figcaption>{{photo.name}} - {{photo.appareil}}</figcaption>
          </a>
        </td>
   {% if forloop.last %}
     </tr>
   {% else %}
     {% if forloop.counter|divisibleby:"3" %}
       </tr><tr>
     {% endif %}
   {% endif %}
{% endfor %}
</table>

{% endblock %}

```
### Modifications éventuelles
- Au besoin modifier la valeur de `divisibleby` dans `forloop.counter` en fonction du nombre de photos à afficher par ligne
### Sauvegarder et fermer
## Ajouter un bouton dans la page `Accueil`
### Ouvrir `accueil.html` en écriture 
```sh
nano ~/folder/project/camera/templates/camera/accueil.html
```
### Ajouter le bouton
- Juste avant `{% endblock %}` ou bien insérée entre deux balises `<a>...</a>`
- Ajouter la ligne 
```html
<a href="/camera/nuitParMinute/" class="button">Nuit par Minute</a>
```
- au besoin ajouter une balise `<br>` pour un saut de ligne
## Relancer la raspberry
```sh
sudo reboot
```