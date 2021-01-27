---
title: "wsgi.py"
date: 2021-01-24T20:34:32+01:00
draft: false
---

```python
"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

sys.path.append('/home/pi/folder/project')
sys.path.append('/home/pi/folder/project/project')

application = get_wsgi_application()
```
