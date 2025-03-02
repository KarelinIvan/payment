from django.urls import path
from product.views import get_stripe_session_id, get_item_html, success, cancel
from product.apps import ProductConfig

app_name = ProductConfig.name

urlpatterns = [
    path('buy/<int:item_id>/', get_stripe_session_id, name='get_stripe_session_id'),
    path('item/<int:item_id>/', get_item_html, name='get_item_html'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
]
