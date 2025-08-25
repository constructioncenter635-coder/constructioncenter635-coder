from pathlib import Path
from decimal import Decimal
import dj_database_url
import os

# Base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta y debug
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "center2025")
DEBUG = True
ALLOWED_HOSTS = ["*"]  # En producción, especificar dominios reales

# Aplicaciones instaladas
INSTALLED_APPS = [
    # apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # tu app inventario
    'inventario',

    # widget tweaks
    'widget_tweaks',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise para estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'ferreteria_web_project.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'ferreteria_web_project.wsgi.application'

# Base de datos
if os.getenv("RENDER") == "true":
    # PostgreSQL en Render
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv('DATABASE_URL', 'postgresql://ferreteria_user:9eHX65ewvyXkCkPVciEufttwEnpEUGtc@dpg-d2lrf9vdiees73ca0nb0-a:5432/ferreteria_db_3ft9'),
            conn_max_age=600
        )
    }
else:
    # Local: SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Tamaño máximo de subida
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Configuración adicional
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

# SmartClick
SMARTCLICK_URL = "TU_URL_REAL_DE_SMARTCLICK"
SMARTCLICK_METHOD = "GET"  # o POST según tu integración
SMARTCLICK_API_KEY = "TU_API_KEY_DE_SMARTCLICK"

# Constantes
TAX_RATE = Decimal('0.18')  # IGV 18%
