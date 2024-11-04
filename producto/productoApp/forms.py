# productoApp/forms.py

from django import forms
from productoApp.models import Productos, Distribuidor, Factura
class FormProducto(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombreProducto', 'descripcion', 'categoria', 'denominacionOrigen', 'cantidadProducto', 'distribuidores', 'facturas']
        widgets = {
            'nombreProducto': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'denominacionOrigen': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'cantidadProducto': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'distribuidores': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'facturas': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class FormDistribuidor(forms.ModelForm):
    class Meta:
        model = Distribuidor
        fields = '__all__'
        widgets = {
            'fechaDespacho': forms.DateInput(attrs={'type': 'date'}),
            'fechaRecepcion': forms.DateInput(attrs={'type': 'date'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de Teléfono',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo Electrónico',
                'required': 'required'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad',
                'required': 'required'
            }),
            'fechaDespacho': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fechaRecepcion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def clean_telefono(self):
         telefono = self.cleaned_data.get('telefono')
         if not telefono.isdigit():
             raise forms.ValidationError(('El número de teléfono debe contener solo dígitos.'))
         if len(telefono) < 10:
             raise forms.ValidationError(('El número de teléfono debe tener al menos 10 dígitos.'))
         return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Distribuidor.objects.filter(email=email).exists():
            raise forms.ValidationError(('Este correo electrónico ya está en uso.'))
        return email

    def clean(self):
        super().clean()
        fecha_despacho = self.cleaned_data.get('fechaDespacho')
        fecha_recepcion = self.cleaned_data.get('fechaRecepcion')
        if fecha_despacho and fecha_recepcion and fecha_despacho > fecha_recepcion:
            self.add_error('fechaRecepcion', ('La fecha de recepción debe ser igual o posterior a la fecha de despacho.'))
class FormFactura(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
           
            'fechaFacturacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'precioUnitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio Unitario',
                'required': 'required'
            }),
            'iva': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'IVA (%)',
                'required': 'required'
            }),
            'descuentoTotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descuento Total',
                'required': 'required'
            }),
        }