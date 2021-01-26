---
title: "stream_1.html"
date: 2021-01-24T16:29:38+01:00
draft: false
---

```html
{% extends "camera/base.html" %}

{% block content %}
<h2 class="monh2">Caméra 1 en direct</h2>

<figure>
    <img class="centre-image imgresponsive" src={{stream.0}} alt="Erreur sur la caméra 1" width="300" > 
    <figcaption>CAMERA 1 : Streaming</figcaption>
    </figure>
    
<br><br><br>

<a class="buttonLigne" href="/camera/stream_AllCam/">Direct 3 Caméras</a>
<a class="buttonLigne" href="/camera/">Accueil</a>

{% endblock %}
```
