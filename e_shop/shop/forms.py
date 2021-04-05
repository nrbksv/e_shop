from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput
from django import forms

from shop.models import Product, Order, ProductCart


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'product', 'description', 'price', 'balance']

        widgets = {
            'category': Select(attrs={
                'class': 'form-control'
            }),
            'product': TextInput(attrs={
                'class': 'form-control'
            }),
            'description': Textarea(attrs={
                'class': 'form-control'
            }),
            'price': NumberInput(attrs={
                'class': 'form-control'
            }),
            'balance': NumberInput(attrs={
                'class': 'form-control'
            }),
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user_name', 'user_address', 'user_phone']

        widgets = {
            'user_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'user_address': TextInput(attrs={
                'class': 'form-control'
            }),
            'user_phone': TextInput(attrs={
                'class': 'form-control'
            })
        }


# class ProductCartForm(ModelForm):
#     class Meta:
#         model = ProductCart
#         fields = ['quantity']