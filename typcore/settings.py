import os
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# 1. DIRETÓRIOS E PATHS
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Isso permite que o Django enxergue 'products' e 'customers' diretamente
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 2. SEGURANÇA BÁSICA
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-typcore-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '.typcore.com.br', 
    'typcore.com.br', 
    'localhost', 
    '127.0.0.1',
    '.railway.app', 
]

# 3. DEFINIÇÃO DE APPS (Removido o prefixo 'apps.' pois sys.path já aponta para a pasta)
# 1. Primeiro defina a SHARED_APPS
SHARED_APPS = [
    'jazzmin',
    'django_tenants',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.customers', # Caminho completo
    
]

# 2. Depois defina a TENANT_APPS
TENANT_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'apps.products',  # Caminho completo
    
    ]
    

# 3. POR ÚLTIMO você faz a soma (Linha 43 que deu erro)
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]# 4. CONFIGURAÇÃO MULTI-TENANT
TENANT_MODEL = "customers.Client"
TENANT_DOMAIN_MODEL = "customers.Domain"

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware', # Sempre o primeiro
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'typcore.urls'
PUBLIC_SCHEMA_URLCONF = 'typcore.urls'

# 5. BANCO DE DADOS
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# 6. TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# 7. ESTÁTICOS
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 8. INTERNACIONALIZAÇÃO
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 9. SEGURANÇA DE COOKIES E HTTPS (Fundamental para o Brasil/Cloudflare)
CSRF_TRUSTED_ORIGINS = [
    'https://*.up.railway.app',
    'https://erp.typcore.com.br',
    'https://*.typcore.com.br', # Permite todos os subdomínios dos clientes
]

TENANT_USERS_DOMAIN_ALLOW_ALL = True 

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = None
    CSRF_COOKIE_DOMAIN = None