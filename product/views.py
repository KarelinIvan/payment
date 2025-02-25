import os

import stripe
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from product.models import Item

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


@api_view(['GET'])
def get_item(request, pk):
    """ Извлекает элемент из базы данных на основе предоставленного первичного ключа,
    и отображает его с использованием связанного с ним HTML-шаблона """
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    return render(request, 'product/item.html', {'item': item})


@api_view(['GET'])
def create_session(request, pk):
    """ Создает сеанс оформления заказа Stripe для указанного продукта """
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

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
        success_url='http://example.com/success',
        cancel_url='http://example.com/cancel',
    )
    return JsonResponse({'session_id': session.id})
