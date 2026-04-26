"""
Django settings for core project.
Universal configuration - works on localhost, Codespace, Railway, VPS, Docker, etc.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# ENVIRONMENT DETECTION (Universal)
# ==========================================
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
ON_CODESPACE = os.getenv("ON_CODESPACE", "False") == "True"

# ==========================================
# SECURITY - SECRET KEY
# ==========================================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'dev-unsafe-key-only-for-development'
        import warnings
        warnings.warn("DJANGO_SECRET_KEY not set. Using unsafe development key.")
    else:
        raise ValueError(
            "DJANGO_SECRET_KEY environment variable must be set in production. "
            "Generate one with: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
        )

# ==========================================
# ALLOWED HOSTS (Universal - Environment Variable)
# ==========================================
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS]  # Clean whitespace

# For Codespace: Add dynamic domain
if ON_CODESPACE:
    codespace_name = os.getenv("CODESPACE_NAME")
    codespace_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    if codespace_name and codespace_domain:
        ALLOWED_HOSTS.append(f'{codespace_name}-8000.{codespace_domain}')
        ALLOWED_HOSTS.append('.app.github.dev')

# ==========================================
# FRONTEND URL (Universal - Environment Variable)
# ==========================================
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

if not FRONTEND_URL and not DEBUG:
    raise ValueError("FRONTEND_URL environment variable must be set in production")

# ==========================================
# DATABASE (Universal - Environment Variable)
# ==========================================
database_url = os.getenv('DATABASE_URL', '')

if database_url:
    # Use provided database URL (PostgreSQL)
    tmpPostgres = urlparse(database_url)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path.replace('/', ''),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': tmpPostgres.port or 5432,
            'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
        }
    }
else:
    # Fallback to local SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    
    # ALLAUTH APPS
    'allauth',
    'allauth.account',
    'allauth.headless',
    
    # Local apps
    'api',
    'commando',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

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

# ==========================================
# ALLAUTH HEADLESS SETTINGS
# ==========================================
# Use custom form for registration
ACCOUNT_SIGNUP_FORM_CLASS = 'api.forms.CustomSignupForm'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['username', 'email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[arvebCRM] '

HEADLESS_ONLY = True
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": f"{FRONTEND_URL}/verify-email/{{key}}",
    "account_reset_password_from_key": f"{FRONTEND_URL}/password-reset/{{key}}",
}

HEADLESS_ADAPTER = 'api.adapters.CustomHeadlessAdapter'

# ==========================================
# CORS & CSRF (Universal - Environment Variables)
# ==========================================
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(',')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS]

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(',')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS]

# For Codespace: Add dynamic origins
if ON_CODESPACE:
    codespace_name = os.getenv("CODESPACE_NAME")
    codespace_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    
    if codespace_name and codespace_domain:
        frontend_url = f"https://{codespace_name}-5173.{codespace_domain}"
        backend_url = f"https://{codespace_name}-8000.{codespace_domain}"
        
        CORS_ALLOWED_ORIGINS.append(frontend_url)
        CSRF_TRUSTED_ORIGINS.append(backend_url)
        
        # Update headless URLs for Codespace
        HEADLESS_FRONTEND_URLS = {
            "account_confirm_email": f"{frontend_url}/verify-email/{{key}}",
            "account_reset_password_from_key": f"{frontend_url}/password-reset/{{key}}",
        }
    
    # Codespace-specific middleware
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    INSTALLED_APPS += ['django_browser_reload']
    MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']
    X_FRAME_OPTIONS = 'ALLOW-FROM preview.app.github.dev'

# ==========================================
# INTERNATIONALIZATION
# ==========================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kuala_Lumpur'
USE_I18N = True
USE_TZ = True

# ==========================================
# STATIC FILES & MEDIA
# ==========================================
STATIC_URL = 'static/'
STATICFILES_BASE_DIR = BASE_DIR / 'staticfiles'
STATICFILES_BASE_DIR.mkdir(exist_ok=True, parents=True)

STATICFILES_VENDOR_DIR = STATICFILES_BASE_DIR / 'vendors'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [STATICFILES_BASE_DIR]
STATIC_ROOT = BASE_DIR / 'local-cdn'

# ==========================================
# SECURITY SETTINGS (Production)
# ==========================================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Proxy headers for reverse proxies (Nginx, Railway, etc.)
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ==========================================
# REST FRAMEWORK
# ==========================================
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '1000/day',
    }
}

# ==========================================
# LOGGING (Production)
# ==========================================
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

# ==========================================
# CUSTOM USER MODEL
# ==========================================
AUTH_USER_MODEL = 'api.User'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'