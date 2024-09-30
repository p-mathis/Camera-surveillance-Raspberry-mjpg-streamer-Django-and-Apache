---
title: "nuit.html"
date: 2021-01-24T16:29:17+01:00
draft: false
---

```html
{% extends "camera/base.html" %}
{% load static %}

{% block header %}
<h1 class="monh1">Photos de nuit</h1>
<pre>
  Coucher : {% if horaire %}{{ horaire.3 }} - le {{horaire.4}}/{{horaire.5}}{% endif %}
  Lever   : {% if horaire %}{{ horaire.0 }} - le {{horaire.1}}/{{horaire.2}}{% endif %}
  
  </pre>
{% endblock %}

{% block content %}

<table>
    <tr>
    {% for photo in night_photo_list_oneoutofN %}
        <td>
          <a href="{% static photo.file_photo_jpg %}">
          <img class="centre-image imgresponsive" src="{% static photo.file_photo_jpg %}" height="150" width="225" alt="photo nocturne indisponible" loading="lazy"/><figcaption>{{photo.name}} - {{photo.appareil}}</figcaption>
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
