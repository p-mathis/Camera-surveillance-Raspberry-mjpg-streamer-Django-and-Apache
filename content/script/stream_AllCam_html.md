---
title: "stream_AllCam.html"
date: 2021-01-24T16:30:17+01:00
draft: false
---

```html
{% extends "camera/base.html" %}

{% block content %}

<h1 class="monh1">les 3 caméras en direct</h2>

<table>
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
<td>
<a href="{% url 'stream_2' %}">

        <img class="centre-image imgresponsive" src={{stream.1}} alt="Erreur sur la caméra 2" width="300" >        
         
        <figcaption>CAMERA 2 : Streaming</figcaption>

</a>
</td>
</tr>
</table>

{% endblock %}
```
