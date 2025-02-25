from django import forms

from product.models import Item


class ItemForm(forms.ModelForm):
    """ Форма добавления продукта """

    class Meta:
        model = Item
        fields = ('name', 'price', 'description')
