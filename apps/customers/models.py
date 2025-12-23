from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

# 1. Modelo de Ramo de Atividade
class BusinessSector(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 2. Modelo de Cliente (Apenas UMA vez)
class Client(TenantMixin):
    name = models.CharField(max_length=100)
    # Conecta ao ramo de atividade
    sector = models.ForeignKey(BusinessSector, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Dados de contato
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    document = models.CharField(max_length=20, blank=True, verbose_name="CPF/CNPJ")
    
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    auto_drop_schema = True 

    def __str__(self):
        return self.name
 

# 3. Modelo de Domínio (Apenas UMA vez)
class Domain(DomainMixin):
    pass