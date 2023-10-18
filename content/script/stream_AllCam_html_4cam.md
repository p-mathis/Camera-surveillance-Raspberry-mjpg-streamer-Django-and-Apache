---
title: "stream_AllCam_4cam"
date: 2023-10-17T16:30:17+01:00
draft: false
---

```html
{% extends "camera/base.html" %}

{% block content %}

<!-- Modifier le titre : les 4 caméras en direct  -->
<h1 class="monh1">les 4 caméras en direct</h2>

<table>
    <!-- Scinder le tableau en 2 lignes (balise <tr>). Ecriture de la première ligne avec 2 cellules (balise >td> -->
    <tr>
        <td>
            <a href="{% url 'stream_py' %}">

                <img class="centre-image imgresponsive" src={{stream.2}} alt="Erreur sur la caméra nocturne" width="300" >
                <figcaption>CAMERA Nuit : Streaming</figcaption>
            </a>
        </td>
        <td>
            <a href="{% url 'stream_1' %}">        
                <img class="centre-image imgresponsive" src={{stream.0}} alt="Erreur sur la caméra 1" width="300" >        
                <figcaption>CAMERA 1: Streaming</figcaption>
       
            </a>
        </td>
        <!-- Fin de la première ligne  -->
        <!-- Ecriture de la deuxième ligne : conservation de la cellule existante et ajout de la cellule pour la quatrième caméra -->
        <td>
            <a href="{% url 'stream_2' %}">
                <img class="centre-image imgresponsive" src={{stream.1}} alt="Erreur sur la caméra 2" width="300" >       
                <figcaption>CAMERA 2 : Streaming</figcaption>
            </a>
        </td>
        <!-- Ajout de la cellule de la quatrième caméra -->
        <td>
            <a href="{% url 'stream_3' %}">      
                <img class="centre-image imgresponsive" src={{stream.3}} alt="Erreur sur la caméra 3" width="300" >    
                <figcaption>CAMERA 3 : Streaming</figcaption>
            </a>
        </td>
        <!-- Fin d'ajout de la cellule de la quatrième caméra -->
    </tr>
    <!-- Fin de la deuxième ligne -->
</table>

{% endblock %}
```
