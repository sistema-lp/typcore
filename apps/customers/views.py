from django.shortcuts import render
from django.views.generic import ListView
from .models import Client # Ou o nome do seu modelo de Tenant
from products.models import Product

class ClientListView(ListView):
    model = Client
    template_name = 'customers/client_list.html'
    context_object_name = 'clients'


def dashboard_view(request):
    total_products = Product.objects.count()
    total_clients = Client.objects.count()
    
    context = {
        'total_products': total_products,
        'total_clients': total_clients,
    }
    return render(request, 'dashboard.html', context)