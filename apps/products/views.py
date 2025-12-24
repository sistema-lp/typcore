from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html' # O Django vai procurar em templates/products/