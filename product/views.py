from product.models import Item
from product.forms import ItemForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

class PostListView(ListView):
    """ Просмотр всех продуктов"""
    model = Item
    template_name = ''
    context_object_name = 'products'


class PostDetailView(DetailView):
    """ Просмотр продукта """
    model = Item
    template_name = ''
    context_object_name = 'product'


class PostUpdateView(UpdateView):
    """ Изменение продукта """
    model = Item
    form_class = ItemForm
    template_name = ''
    success_url = reverse_lazy('')


class PostDeleteView(DeleteView):
    """ Удаление продукта """
    model = Item
    template_name = ''
    success_url = reverse_lazy('')
