from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    """ Модель продукта """
    name = models.CharField(max_length=100, verbose_name='Наименование продукта',
                            help_text='Укажите наименование продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', help_text='Укажите цену продукта',
                                validators=[MinValueValidator(0)])
    description = models.TextField(verbose_name='Описание продукта', help_text='Укажите описание продукта')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
