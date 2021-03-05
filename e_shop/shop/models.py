from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('appliances', 'Бытовая техника'),
        ('smartphones', 'Смартфоны'),
        ('laptops', 'Ноутбуки'),
        ('tablets', 'Планшеты'),
        ('other', 'Разное')
    ]

    product = models.CharField(max_length=100, blank=False, null=False, verbose_name='Наименование товара')
    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Описание')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other', blank=False, null=False, verbose_name='Категория')
    balance = models.PositiveIntegerField(verbose_name='Остаток')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


    def __str__(self):
        return f'{self.product} {self.category} {self.description} {self.price} {self.balance}'
