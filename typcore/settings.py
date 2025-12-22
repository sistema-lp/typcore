import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv # Adicione esta linha
import sys

load_dotenv() # E esta também

BASE_DIR = Path(__file__).resolve().parent.parent
# ADICIONE ESTA LINHA:
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-typcore-key')
DEBUG = False
# O ponto antes de .typcore.com.br é o segredo para aceitar todos os subdomínios
ALLOWED_HOSTS = [
    '.typcore.com.br', 
    'typcore.com.br', 
    'localhost', 
    '127.0.0.1',
    '.railway.app', # Caso você ainda use o domínio do Railway para testes
]
TENANT_MODEL = "customers.Client"   # Se a sua pasta for 'apps/customers', use "apps_customers.Client"
DOMAIN_MODEL = "customers.Domain"   # Ajuste conforme o nome da app no INSTALLED_APPS

SHARED_APPS = [
    'jazzmin',
    'django_tenants',
    'apps.customers',    # <-- Use o caminho da pasta direto
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
    'apps.products',     # <-- Use o caminho da pasta direto
]

# AQUI ESTÁ O SEGREDO: Use o caminho COMPLETO para o modelo
TENANT_MODEL = 'apps_customers.Client' 
DOMAIN_MODEL = 'apps_customers.Domain'

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# O MODELO DEVE USAR O LABEL:
TENANT_MODEL = 'customers.Client' 
DOMAIN_MODEL = 'customers.Domain'
# Mantenha exatamente assim:
TENANT_MODEL = 'customers.Client' 
DOMAIN_MODEL = 'customers.Domain'
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]


# 2. MIDDLEWARE (A ordem aqui é vital)
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware', # ATIVADO
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# PADRÕES
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CSRF_TRUSTED_ORIGINS = ['https://web-production-80309.up.railway.app']
    
# Permite que o Django reconheça o domínio mesmo se houver subdomínios extras
TENANT_ALLOW_MAIN_DOMAIN_USER_REGISTRATION = True

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

        import os

# Caminho onde o Django buscará arquivos estáticos adicionais
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Pasta onde o Django vai reunir todos os estáticos para o Railway usar
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
JAZZMIN_SETTINGS = {
    "site_title": "TypCore ERP",
    "site_header": "TypCore",
    "site_brand": "TypCore Admin",
    "site_logo": "img/logo_typcore.png", 
    "login_logo": None,
    "welcome_sign": "Bem-vindo ao TypCore ERP",
    "copyright": "TypCore Ltda",
    "search_model": ["customers.Client"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Início", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "customers.Client": "fas fa-building",
        "customers.Domain": "fas fa-link",
        "customers.BusinessSector": "fas fa-briefcase",
        "products.Product": "fas fa-box-open",
    },
}

JAZZMIN_UI_CONFIG = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
}
        
# Configurações de Segurança para Produção
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000 # 1 ano de HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    
   # Permite que o cookie de sessão funcione em todos os subdomínios
SESSION_COOKIE_DOMAIN = '.typcore.com.br'

# Se você estiver usando HTTPS (o Railway fornece por padrão), adicione:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')