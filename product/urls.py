from django.urls import path

from product.apps import ProductConfig
from product.views import GetItemView, CreateSessionView

app_name = ProductConfig.name

urlpatterns = [
    path('product/<int:pk>/', GetItemView.as_view(), name='product'),
    path('create-session/<int:pk>/', CreateSessionView.as_view(), name='create_session'),
]
