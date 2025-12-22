from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # O campo auto_drop_schema garante que ao deletar um cliente, o esquema suma
    auto_drop_schema = True 

class Domain(DomainMixin):
    pass