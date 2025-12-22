from apps.customers.views import home # Importe a view que criamos

urlpatterns = [
    path('', home, name='home'), # Página inicial agora é a 'home'
    path('admin/', admin.site.urls),
]