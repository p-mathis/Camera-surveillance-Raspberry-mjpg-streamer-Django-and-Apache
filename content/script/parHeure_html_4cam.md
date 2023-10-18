---
title: "parHeure_4cam.html"
date: 2023-10-17T16:39:07+01:00
draft: false
---

```html
{% extends "camera/base.html" %}

{% load static %}


{% block header %}
<h1 class="monh1">Photos par Heures</h1><br>

{% endblock %}

{% block content %}

<p class="monh2">Page {{ photos.number }} / {{ photos.paginator.num_pages }}</p> 

{% if photos.has_previous %}
<a class="buttonLigne" 
href="?page={{ photos.previous_page_number }}">Page Précédente</a>
{% endif %}
{% if photos.has_next %}
<a class="buttonLigne" 
href="?page={{ photos.next_page_number }}">Page Suivante</a>
{% endif %}

<table>
    <tr>
    {% for photo in photos %}
        <td><img class="centre-image imgSmall" src="{% static photo.file_photo_jpg %}" height="150" width="225" alt="photo non disponible"/><figcaption>{{photo.name}} - {{photo.appareil}}</figcaption>
        </td>
   {% if forloop.last %}
     </tr>
   {% else %}
   <!-- Modifier la valeur pour forloop.counter en mettant `4` ou `2` ou bien la laisser inchangée  -->
     {% if forloop.counter|divisibleby:"4" %}
       </tr><tr>
     {% endif %}
   {% endif %}
{% endfor %}
</table>
<br>

{% if photos.has_other_pages %}
  <ul class="pagination">
    {% if photos.has_previous %}
      <li><a href="?page={{ photos.previous_page_number }}">précédent</a></li>
      {% else %}
      <li class="disabled"><span>&laquo;</span></li>
    {% endif %}
    {% for i in photos.paginator.page_range %}
      {% if photos.number == i %}
        <li class="liActive"></li>
      {% else %}
        <li><a href="?page={{ i }}">{{ i }}</a></li>
      {% endif %}
    {% endfor %}
    {% if photos.has_next %}
      <li><a href="?page={{ photos.next_page_number }}">suivant</a></li>
    {% else %}
      <li class="disabled"><span>&raquo;</span></li>
    {% endif %}
  </ul>
  <br><br>
  <span class="spanPage">
    Page {{ photos.number }} de {{ photos.paginator.num_pages }}.
  </span>
{% endif %}

{% endblock %}
```
