---
title: "accueil.html"
date: 2021-01-24T16:28:53+01:00
draft: false
---

```html
{% extends "camera/base.html" %}

{% block content %}

<div class="grid-One">
        <div>Bienvenue sur le site de X&Y !!<br>
        Choisissez la page que vous souhaitez consulter.
        </div>
</div>

        <a href="/camera/stream_AllCam/" class="button">En direct</a><br>
        <a href="/camera/nuit/" class="button">Nuit</a><br>
        <a href="/camera/historique/" class="button">Historique</a><br>
        <a href="/camera/parHeure/" class="button">Heure par Heure</a><br>


{% endblock %}
```
