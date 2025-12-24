from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # O "apps." antes do nome garante que o Django encontre a pasta correta
    path('products/', include('apps.products.urls')),
    path('customers/', include('apps.customers.urls')),
]