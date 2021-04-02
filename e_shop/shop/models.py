from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    product = models.CharField(max_length=100, blank=False, null=False, verbose_name='Наименование товара')
    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Описание')
    category = models.ForeignKey('shop.Category', on_delete=models.PROTECT, related_name='products', default=1, verbose_name='Категория')
    balance = models.PositiveIntegerField(verbose_name='Остаток', validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.product}{self.category}{self.description} {self.price} {self.balance}'


class Category(models.Model):
    category = models.CharField(max_length=100, blank=False, null=False, verbose_name='Категория')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.category}'
