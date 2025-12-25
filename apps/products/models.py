from django.db import models

class Product(models.Model):
    # Deixe o Django criar o ID sozinho no banco novo
    name = models.CharField(max_length=255, verbose_name="Nome do Produto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")

    class Meta:
        app_label = 'products'
        db_table = 'products_product' 

    def __str__(self):
        return self.name