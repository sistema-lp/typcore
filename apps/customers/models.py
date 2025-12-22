from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # O campo auto_drop_schema garante que ao deletar um cliente, o esquema suma
    auto_drop_schema = True 

class Domain(DomainMixin):
    pass

# Adicione isso no topo ou junto com os modelos de Clientes
class BusinessSector(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name