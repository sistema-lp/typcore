from django.contrib import admin
from django.urls import path # ESTA LINHA ESTÁ FALTANDO OU COM ERRO
from apps.customers.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]