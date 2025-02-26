import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View

from product.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    """ Вьюсет для создания сессии оплаты Stripe """

    def get(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        item = get_object_or_404(Item, id=item_id)
        domain = "http://130.193.52.110:8082"  # here must be actual domain
        if settings.DEBUG:
            domain = "http://127.0.0.1:8082"
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        "price_data": {
                            "currency": item.currency,
                            "product_data": {"name": item.name},
                            "unit_amount": int(item.price * 100),  # convert dollars into cents
                        },
                        "quantity": 1,
                    },
                ],
                mode='payment',
                success_url=f'{domain}/payment_success/',
                cancel_url=f'{domain}/payment_failed/',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as err:
            print(err)  # should be in logs
            return JsonResponse({'error': str(err)})


class ItemView(View):
    """ Вьюсет для просмотра продукта """
    template_name = 'product/item.html'

    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        context = {'item': item,
                   'strip_public_key': settings.STRIPE_PUBLISHABLE_KEY
                   }
        return render(request, self.template_name, context)
