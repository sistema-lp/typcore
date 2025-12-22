from django.apps import AppConfig  # <--- ADICIONE AQUI TAMBÉM

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    label = 'products'