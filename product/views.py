from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.exceptions import NotFound

from config.settings import STRIPE_SECRET_KEY
from .models import Item
import stripe

stripe.api_key = STRIPE_SECRET_KEY

class BuyItemView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/buy.html'

    def get(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise NotFound("Item does not exist")

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )

        return Response({
            'session_id': session.id,
            'secretKey': stripe.api_key,
        })

class ItemDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/item_detail.html'

    def get(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise NotFound("Item does not exist")

        return Response({
            'item': item,
        })