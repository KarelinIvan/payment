from django.shortcuts import render
from django.http import JsonResponse
import stripe
from config import settings
from product.models import Item


def get_stripe_session_id(request, item_id):
    item = Item.objects.get(pk=item_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'id': session.id})


def get_item_html(request, item_id):
    item = Item.objects.get(pk=item_id)
    publishable_key = settings.PUBLIC_STRIPE_SECRET_KEY
    return render(request, 'product/item.html', {'item': item, 'publishable_key': publishable_key})


def success(request):
    return render(request, 'product/success.html')


def cancel(request):
    return render(request, 'product/cancel.html')