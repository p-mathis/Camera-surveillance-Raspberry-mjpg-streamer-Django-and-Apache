---
title: "stream.3_4cam_html"
date: 2023-10-18T16:29:44+01:00
draft: false
---

```html
{% extends "camera/base.html" %}

{% block content %}
<h2 class="monh2">Caméra 3 en direct</h2>

<figure>
    <img class="centre-image imgresponsive" src={{stream.0}} alt="Erreur sur la caméra 3" width="300" > 
    <figcaption>CAMERA 3 : Streaming</figcaption>
    </figure>

<br><br><br>    

<a class="buttonLigne" href="/camera/stream_AllCam/">Direct 4 Caméras</a>
<a class="buttonLigne" href="/camera/">Accueil</a>

{% endblock %}
```
