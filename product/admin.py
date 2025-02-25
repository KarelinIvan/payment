from django.contrib import admin
from product.models import Item

# Register your models here.
@admin.register(Item)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

