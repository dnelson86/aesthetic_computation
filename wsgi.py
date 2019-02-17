"""
WSGI config (DEVELOPMENT) for Aesthetic Computation.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aesthetic_computation.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

