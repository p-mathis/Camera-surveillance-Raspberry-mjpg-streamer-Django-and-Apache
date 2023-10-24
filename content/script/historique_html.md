---
title: "historique.html"
date: 2021-01-24T16:29:06+01:00
draft: false
---

```html
{% extends "camera/base.html" %}
{% load static %}

{% block header %}
<h1 class="monh1">Historique Général</h1>

{% endblock %}

{% block content %}

<table>
  <tr>
  {% for photo in latest_photo_list_group %}
      <td>
        <a href="{% static photo.file_photo_jpg %}">
        <img class="centre-image imgresponsive" src="{% static photo.file_photo_jpg %}" height="150" width="225" alt="photo non disponible" loading="lazy"/><figcaption>{{photo.name}} - {{photo.appareil}}</figcaption>
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
