import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OIL_PAINTING_BE.settings')

application = get_asgi_application()
