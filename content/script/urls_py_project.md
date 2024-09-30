---
title: "urls.py (project)"
date: 2021-01-24T10:28:12+01:00
draft: false
---

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
path('camera/', include('camera.urls')),
path('admin/', admin.site.urls),
]
```
