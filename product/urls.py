from django.urls import path

from product.apps import ProductConfig
from product.views import get_item, create_session

app_name = ProductConfig.name

urlpatterns = [
    path('product/<int:pk>/', get_item, name='product'),
    path('buy/<int:pk>/', create_session, name='create_session'),
]
