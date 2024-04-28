import os

from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from django.core.asgi import get_asgi_application
from . import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
application = get_asgi_application()
app = Starlette(debug=True, routes=[
    Mount('/static', StaticFiles(directory=settings.BASE_DIR / 'static'), name='/static/'),
    Mount('/media', StaticFiles(directory=settings.BASE_DIR / 'media'), name='/media/'),
])

app.mount('/', application)
