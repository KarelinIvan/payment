from product.models import Item
import stripe
import os
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


@api_view(['GET'])
def get_product(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        context = {'product': item}
        return render(request,item.html,context)
    except Item.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
def create_session(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        checkout_session = stripe.checkout.Session.create(
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
            success_url='http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8000/cancel',
        )
        return Response({'session_id': checkout_session.id})
    except Exception as e:
        return Response(str(e), status=HTTP_400_BAD_REQUEST)

