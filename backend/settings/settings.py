import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = True if os.environ['DJANGO_DEBUG'] == '1' else False

ALLOWED_HOSTS = [host for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')]

CSRF_TRUSTED_ORIGINS = [host for host in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = False

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'admin_interface',
    'colorfield',
    'custom_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    "corsheaders",
    'django_celery_beat',
    'rest_framework',
    'ps_store_api',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'custom_admin' / 'templates'],
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings.context_processors.custom_settings',
            ],
        },
    },
]

ASGI_APPLICATION = 'settings.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://redis:6379/3"],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://redis:6379/1"
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CELERY_BROKER_URL = "redis://redis:6379/3"
CELERY_RESULT_BACKEND = "redis://redis:6379/4"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

ADMIN_TOOLS_INDEX_DASHBOARD = 'custom_admin.dashboard.CustomIndexDashboard'

ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'custom_admin.dashboard.CustomAppIndexDashboard'

ADMIN_TOOLS_MENU = 'custom_admin.menu.CustomMenu'

FORCE_SCRIPT_NAME = os.environ.get('DJANGO_BASE_URL', '/')

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_ROOT.mkdir(exist_ok=True)

STATIC_ROOT.mkdir(exist_ok=True)

TELEGRAM_BOT_SCHEMA = os.environ.get('TELEGRAM_BOT_SCHEMA')

TELEGRAM_BOT_HOST = os.environ.get('TELEGRAM_BOT_HOST')

TELEGRAM_BOT_PORT = int(os.environ.get('TELEGRAM_BOT_PORT'))

TELEGRAM_BOT_URL = f'{TELEGRAM_BOT_SCHEMA}://{TELEGRAM_BOT_HOST}{f":{TELEGRAM_BOT_PORT}" if TELEGRAM_BOT_PORT else ""}'

PAYMENTS_URL = f'{os.environ.get("PAYMENTS_SCHEMA")}://{os.environ.get("PAYMENTS_HOST")}'
if os.environ.get("PAYMENTS_PORT"):
    PAYMENTS_URL += f':{os.environ.get("PAYMENTS_PORT")}'
