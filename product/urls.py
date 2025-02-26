from django.urls import path

from product.views import CreateCheckoutSessionView, ItemView

urlpatterns = [
    path('buy/<int:item_id>/', CreateCheckoutSessionView.as_view(), name='buy_item'),  # create a checkout session
    path('item/<int:item_id>/', ItemView.as_view(), name='item'),
]
