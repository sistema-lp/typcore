from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome do Produto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")

    class Meta:
        db_table = 'products_product' # Forçamos o nome para evitar conflitos antigos

    def __str__(self):
        return self.name