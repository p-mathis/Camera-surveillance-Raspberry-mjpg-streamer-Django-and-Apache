---
title: "base.html"
date: 2021-01-24T16:22:37+01:00
draft: false
---

```html
{% load static %}

<!DOCTYPE html>
<html lang="fr">
<head>
  {% block title %}<title>X & Y</title>{% endblock %}
  <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">

  <link rel="stylesheet" href="{% static 'camera/css/general.css' %}">
  <link rel="stylesheet" href="{% static 'camera/css/menu.css' %}">
  <link rel="shortcut icon" href="{% static 'camera/logo/logo.png' %}" type="image/x-icon" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

  <link rel="stylesheet" href="{% static 'camera/css/header_footer.css' %}">
  <link rel="stylesheet" href="{% static 'camera/css/disposition.css' %}">
  <link rel="stylesheet" href="{% static 'camera/css/bouton.css' %}">
  <link rel="stylesheet" href="{% static 'camera/css/pagination.css' %}">
</head>

<script>
  function myFunction() {
    var x = document.getElementById("myNavbar");
    if (x.className === "navbar") {
      x.className += " responsive";
    } else {
      x.className = "navbar";
    }
  }
  </script>

 <body>
  {% block navebar %}

  <div class='navbar' id="myNavbar">
          <ul>
            <li><a href="/camera/" >Accueil</a></li>
            <li class="dropdown"><a class="dropbtn" href="/camera/stream_AllCam/">En Direct &ensp;</a>
            <div class="dropdown-content">
              <a href="/camera/stream_AllCam/">Les 3 Caméras</a>
              <a href="/camera/stream_py/">Caméra Py</a>
              <a href="/camera/stream_1/">Caméra 1</a>
              <a href="/camera/stream_2/">Caméra 2</a>
              </div>
            </li>
            <li><a href="/camera/nuit/">La Nuit</a></li>
            <li><a href="/camera/historique/">Historique</a></li>
            <li><a href="/camera/parHeure/">Par Heures</a></li>
            <div class='icon'>
              <li><a href="javascript:void(0);"  onclick="myFunction()">
                  <i class="fa fa-bars"></i>
                </a>
              </li></div>         
          </ul>
  </div >
  
  {% endblock %}

    <div class= "item_header">
        {% block header %}
        {% endblock %}
    </div>

    <div class="item_main">
    {% block content %}
    {% endblock %}
    </div>

    <table class="item_footer">
    <tr>
        <td><img src="{% static 'camera/logo/logo.png' %}" alt="?logo?"></td>
        <td>Prune & Choco</td>
    </tr>
    </table>
</body>
</html>
