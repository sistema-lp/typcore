import os
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# 1. DEFINIÇÃO DA BASE (DEVE SER A PRIMEIRA COISA)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. CARREGAMENTO DE AMBIENTE
load_dotenv()

# Garante que o Django encontre a pasta 'apps'
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 3. CONFIGURAÇÕES BÁSICAS
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-typcore-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '.typcore.com.br', 
    'typcore.com.br', 
    'localhost', 
    '127.0.0.1',
    '.railway.app', 
]

# 4. DEFINIÇÃO DE APPS (DJANGO-TENANTS)
SHARED_APPS = [
    'jazzmin',
    'django_tenants',
    'apps.customers',    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

TENANT_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'apps.products',     
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "customers.Client"
DOMAIN_MODEL = "customers.Domain"

# 5. MIDDLEWARE
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
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

# 6. BANCO DE DADOS
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

# 7. ARQUIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 8. PADRÕES INTERNACIONAIS
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 9. SEGURANÇA E DOMÍNIOS
CSRF_TRUSTED_ORIGINS = [
    'https://*.up.railway.app',
    'https://erp.typcore.com.br',
    'https://typcore.com.br'
]
TENANT_ALLOW_MAIN_DOMAIN_USER_REGISTRATION = True

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = '.typcore.com.br'

# 10. CONFIGURAÇÃO JAZZMIN
JAZZMIN_SETTINGS = {
    "site_title": "TypCore ERP",
    "site_header": "TypCore",
    "site_brand": "TypCore Admin",
    "welcome_sign": "Bem-vindo ao TypCore ERP",
    "copyright": "TypCore Ltda",
    "icons": {
        "auth": "fas fa-users-cog",
        "customers.Client": "fas fa-building",
        "products.Product": "fas fa-box-open",
    },
}

# 11. SCRIPT DE INICIALIZAÇÃO AUTOMÁTICA (Corrigido para evitar erro de loading)
import django
from django.db.models.signals import post_migrate

def create_public_tenant(sender, **kwargs):
    from apps.customers.models import Client, Domain
    try:
        if not Client.objects.filter(schema_name='public').exists():
            tenant = Client.objects.create(schema_name='public', name='Public Tenant')
            Domain.objects.create(
                domain='erp.typcore.com.br', 
                tenant=tenant, 
                is_primary=True
            )
            print("SUCESSO: Tenant 'public' criado!")
    except Exception as e:
        pass

# Conecta o script ao sinal de pós-migração
post_migrate.connect(create_public_tenant)