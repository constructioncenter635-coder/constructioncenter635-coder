# inventario/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Categoria, Cliente, Sale, SaleItem
from django.forms import modelformset_factory
from decimal import Decimal


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','marca','categoria','cantidad','unidad_medida','precio_compra','porcentaje_ganancia']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'step':'0.01','min':'0'}),
            'precio_compra': forms.NumberInput(attrs={'step':'0.01','min':'0'}),
            'porcentaje_ganancia': forms.NumberInput(attrs={'step':'0.01','min':'0'}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['producto', 'cantidad', 'precio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar nombre, marca y stock en la lista de productos
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['producto'].label_from_instance = lambda obj: f"{obj.nombre} | {obj.marca} | Stock: {obj.cantidad} | Precio: {obj.precio}"
        # Hacer editable el precio
        self.fields['precio'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})