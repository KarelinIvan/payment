import os

import stripe
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

from config import settings

from product.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY



def get_item_from_cache_or_db(pk):
    key = f'item_{pk}'
    item = cache.get(key)
    if not item:
        try:
            item = Item.objects.get(pk=pk)
            cache.set(key, item, timeout=3600)  # Кэшируем на час
        except Item.DoesNotExist:
            pass
    return item

class GetItemView(APIView):
    def get(self, request, pk):
        item = get_item_from_cache_or_db(pk)
        if not item:
            return Response({'error': 'Item not found'}, status=404)
        return render(request, 'product/item.html', {'item': item})


class CreateSessionView(APIView):
    def create_session(self, request, pk):
        """ Создает сеанс оформления заказа Stripe для указанного продукта """
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)

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
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/product/success.html',
            cancel_url='http://localhost:8000/product/cancel.html',
        )
        return session.get('session_id'), session.get('success_url')
