from datetime import timedelta
from pathlib import Path

# 📍 Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔑 SECURITY: Keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ymd)svh6_v00bf95z$57e$-@8*+xet6u*(nijt)6@swbfkhc69'

# 🐞 Debug mode – turn off in production!
DEBUG = True

# 🌐 Allowed hosts for your project
ALLOWED_HOSTS = []

# 🚀 Application definition
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders",
    

    # Custom apps
    'infrastructure.apps.InfrastructureConfig',  # Our infrastructure layer (custom user model, etc.)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",




]

# 🔗 URL Configuration
ROOT_URLCONF = 'config.urls'

# 🎨 Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add template directories here if needed
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

# 🌐 WSGI & ASGI application paths
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# 🗄️ Database configuration (using PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Use a file named "db.sqlite3" in your BASE_DIR
    }
}


# 🔒 Password validation: Use Django's recommended validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# 🌍 Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 🖥️ Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# 🆕 Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 👤 Custom user model (from the infrastructure app)
AUTH_USER_MODEL = 'infrastructure.CustomUser'

# 🔐 Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,  # Uses your Django secret key
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# 🌐 CORS settings (for integration with a frontend like Next.js)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True

# 🔴 Redis settings (for OTPs, caching, etc.)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# ✉️ Email configuration: using console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_FILE_PATH = '/tmp/app-messages'  # Ensure this directory exists
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use database-backed sessions (default)
SESSION_COOKIE_NAME = 'sessionid'  # Default session cookie name
SESSION_COOKIE_AGE = 3600  # Session expiry in seconds (1 hour)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep the session until it expires or user logs out

# Use a secure cookie for sessions in production (optional)
SESSION_COOKIE_SECURE = False  # Set to True in production if using HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookies

# CSRF Settings (important if your app involves sensitive data)
CSRF_COOKIE_SECURE = False  # Set to True in production if using HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookies