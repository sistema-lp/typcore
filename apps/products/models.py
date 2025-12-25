from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome do Produto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")

    class Meta:
        app_label = 'products'
        # Garante que o Django use este nome exato no Postgres
        db_table = 'products_product' 

    def __str__(self):
        return self.name