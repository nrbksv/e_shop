from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput

from shop.models import Product


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