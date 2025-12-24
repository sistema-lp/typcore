from django.urls import path
from .views import ClientListView

app_name = 'customers'

urlpatterns = [
    path('list/', ClientListView.as_view(), name='list'),
]