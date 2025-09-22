"""
Django settings for aureon_core project.
"""
import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CONFIGURAÇÕES PRINCIPAIS
# ==============================================================================
SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-7#*x0#2pc9zd6gc^=l)#+bm+vgt(8*p$l&ovhl5ujmg_m5zj=-')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['127.0.0.1']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ==============================================================================
# APLICAÇÕES
# ==============================================================================
INSTALLED_APPS = [
    # Third-party Apps (devem vir antes do admin)
    'admin_interface',
    'colorfield',
    'nested_admin',

    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Seus Apps
    'core.apps.CoreConfig',
    'contas.apps.ContasConfig',
    'clientes.apps.ClientesConfig',
    'casos.apps.CasosConfig',
    'notificacoes.apps.NotificacoesConfig',
    'equipamentos.apps.EquipamentosConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aureon_core.urls'
WSGI_APPLICATION = 'aureon_core.wsgi.application'

# ==============================================================================
# BANCO DE DADOS
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# ==============================================================================
# TEMPLATES
# ==============================================================================
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
                # A linha 'organizacao.context_processors.empresa_modulos' foi removida
            ],
        },
    },
]

# ==============================================================================
# INTERNACIONALIZAÇÃO E SENHAS
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# ARQUIVOS ESTÁTICOS E DE MÍDIA
# ==============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    "default": { "BACKEND": "django.core.files.storage.FileSystemStorage" },
    "staticfiles": { "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage" },
}

# ==============================================================================
# CONFIGURAÇÕES DE E-MAIL
# ==============================================================================
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ==============================================================================
# CONFIGURAÇÕES DE AUTENTICAÇÃO E OUTRAS
# ==============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# A linha AUTH_USER_MODEL = 'organizacao.Usuario' foi removida

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# --- CONFIGURAÇÕES PARA ADMIN INTERFACE ---
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]