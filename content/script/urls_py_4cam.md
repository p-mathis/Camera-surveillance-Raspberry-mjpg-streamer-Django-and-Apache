---
title: "urls_4cam.py (camera)"
date: 2023-10-17T10:32:54+01:00
draft: false
---

```python
from django.urls import path

from . import views

#Ajouter la quatrième caméra dans urlpatterns[]

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('historique/', views.historique, name='historique'), 
    path('nuit/', views.nuit, name='nuit'),
    path('parHeure/', views.parheure, name='parHeure'),
    path('stream_py/', views.stream_py, name="stream_py"),
    path('stream_1/', views.stream_1, name="stream_1"),
    path('stream_2/', views.stream_2, name="stream_2"),
    path('stream_AllCam/', views.stream_AllCam, name="stream_AllCam"),

    path('stream_3/', views.stream_3, name="stream_3"),
]
```
