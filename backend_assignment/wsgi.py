"""
WSGI config for backend_assignment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from backend_assignment.views import sio
import socketio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_assignment.settings')

application = get_wsgi_application()

application = socketio.WSGIApp(sio, application)
