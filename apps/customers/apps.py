from django.apps import AppConfig

class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.customers'
    label = 'customers'  # Isso força o Django a ignorar a pasta 'apps' no banco