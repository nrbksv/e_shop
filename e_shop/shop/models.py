from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    product = models.CharField(max_length=100, blank=False, null=False, verbose_name='Наименование товара')
    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Описание')
    balance = models.PositiveIntegerField(verbose_name='Остаток', validators=[MinValueValidator(0)])
    category = models.ForeignKey(
        'shop.Category',
        on_delete=models.PROTECT,
        related_name='products',
        default=1,
        verbose_name='Категория'
    )
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.product}'


class Category(models.Model):
    category = models.CharField(max_length=100, blank=False, null=False, verbose_name='Категория')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.category}'


class Order(models.Model):
    product = models.ManyToManyField(
        'shop.Product',
        related_name='order',
        verbose_name='Товары',
        through='shop.OrderProduct',
        through_fields=('order', 'products')
    )
    user_name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Имя')
    user_phone = models.CharField(max_length=20, blank=False, null=False, verbose_name='Телефон')
    user_address = models.CharField(max_length=200, blank=False, null=False, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True)
    _user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', default=None, null=True, verbose_name='Пользователь')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.user_name}  {self.user_phone}  {self.user_address}'


class OrderProduct(models.Model):
    products = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='p_order', verbose_name='Товары')
    order = models.ForeignKey('shop.Order', on_delete=models.CASCADE, related_name='products', verbose_name='Заказ')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        db_table = 'order_products'
        verbose_name = 'Товар/заказ'
        verbose_name_plural = 'Товары/заказ'

    def __str__(self):
        return f'{self.order}{self.products}{self.quantity}'


