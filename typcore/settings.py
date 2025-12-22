import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv # Adicione esta linha

load_dotenv() # E esta também

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-typcore-key')
DEBUG = True
ALLOWED_HOSTS = ['*']

# 1. APPS DO SISTEMA
SHARED_APPS = [
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
    'django.contrib.sessions',
    'django.contrib.messages',
    # Aqui entrarão os módulos dos 20 ramos futuramente
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# 2. MIDDLEWARE (A ordem aqui é vital)
MMIDDLEWARE = [
    # O tenant fica comentado por enquanto
    # 'django_tenants.middleware.main.TenantMainMiddleware', 
    
    'django.middleware.security.SecurityMiddleware',
    
    # ESTA É A LINHA QUE O ERRO PEDIU (Deve vir antes de AuthenticationMiddleware)
    'django.contrib.sessions.middleware.SessionMiddleware', 
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # ESTA DEVE VIR DEPOIS DE SESSIONS
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'typcore.urls'

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

# 3. BANCO DE DADOS
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600  # Mantém a conexão viva por 10 minutos
    )
}

DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

# 4. ROTEAMENTO E MODELOS (O que estava faltando)
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_MODEL = "customers.Client"

TENANT_DOMAIN_MODEL = "customers.Domain"

# PADRÕES
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# No final do seu settings.py
# No final do seu settings.py
import sys

# 1. Garante que o Admin abra mesmo sem tenant configurado
PUBLIC_SCHEMA_URLCONF = 'typcore.urls'

# 2. Script corrigido
if 'gunicorn' in sys.argv[0] or 'runserver' in sys.argv:
    try:
        from django.db import connection
        # ALTERADO: Importando do caminho correto conforme seu SHARED_APPS
        from apps.customers.models import Client, Domain 
        
        if not Client.objects.filter(schema_name='public').exists():
            tenant = Client.objects.create(schema_name='public', name='Public Tenant')
            Domain.objects.create(
                domain='web-production-80309.up.railway.app', 
                tenant=tenant, 
                is_primary=True
            )
            print("SUCESSO: Tenant 'public' criado automaticamente!")
    except Exception as e:
        # Isso vai mostrar o erro real nos Logs do Railway se falhar
        print(f"ERRO NO SCRIPT DE TENANT: {e}")