---
title: "models.py"
date: 2021-01-24T09:39:20+01:00
draft: false
---

```python
from django.db import models
from datetime import datetime

class Appareil(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Photo(models.Model):
    appareil = models.ForeignKey(Appareil, on_delete=models.CASCADE)
    date = models.DateTimeField()    #date de la photo : annee jour mois heure minute
    name = models.CharField(max_length=30)    #nom de la photo tel que dans les dossiers de stockage /stock/camera_xxx
    path = models.CharField(max_length=100)   #nom du dossier où est stockée la photo : camera_xxx ; chemin depuis stock/ (pour être reconnu par Django dans les fichiers static)
    
    def name_photo_jpg(self):
        return "{}.jpg".format(self.name)
    
    def file_photo_jpg(self):
        return "{}/{}.jpg".format(self.path, self.name)
```
